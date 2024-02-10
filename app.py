import streamlit as st
from llm_chains import load_normal_chain, load_pdf_chat_chain
from streamlit_mic_recorder import mic_recorder
from utils import get_timestamp
from image_handler import handle_image
from audio_handler import transcribe_audio
from pdf_handler import add_documents_to_db
from html_templates import css, get_media_template
from database_operations import load_last_k_text_messages, save_text_message, save_image_message, save_audio_message, load_messages, get_all_chat_history_ids, delete_chat_history
import sqlite3
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

@st.cache_resource
def load_chain():
    if st.session_state.pdf_chat:
        print("loading pdf chat chain")
        return load_pdf_chat_chain()
    return load_normal_chain()

def clear_input_field():
    if st.session_state.user_question == "":
        st.session_state.user_question = st.session_state.user_input
        st.session_state.user_input = ""

def set_send_input():
    st.session_state.send_input = True
    clear_input_field()

def toggle_pdf_chat():
    st.session_state.pdf_chat = True

def get_session_key():
    if st.session_state.session_key == "new_session":
        st.session_state.new_session_key = get_timestamp()
        return st.session_state.new_session_key
    return st.session_state.session_key

def delete_chat_session_history():
    delete_chat_history(st.session_state.session_key)
    st.session_state.session_index_tracker = "new_session"

def clear_cache():
    st.cache_resource.clear()

def main():
    st.title("Multimodal Local Chat App")
    st.write(css, unsafe_allow_html=True)
    
    if "send_input" not in st.session_state:
        st.session_state.session_key = "new_session"
        st.session_state.send_input = False
        st.session_state.user_question = ""
        st.session_state.new_session_key = None
        st.session_state.session_index_tracker = "new_session"
        st.session_state.db_conn = sqlite3.connect(config["chat_sessions_database_path"], check_same_thread=False)
        st.session_state.audio_uploader_key = 0
    if st.session_state.session_key == "new_session" and st.session_state.new_session_key != None:
        st.session_state.session_index_tracker = st.session_state.new_session_key
        st.session_state.new_session_key = None

    st.sidebar.title("Chat Sessions")
    chat_sessions = ["new_session"] + get_all_chat_history_ids()

    index = chat_sessions.index(st.session_state.session_index_tracker)
    st.sidebar.selectbox("Select a chat session", chat_sessions, key="session_key", index=index)
    st.sidebar.toggle("PDF Chat", key="pdf_chat", value=False)
    st.sidebar.button("Delete Chat Session", on_click=delete_chat_session_history)
    st.sidebar.button("Clear Cache", on_click=clear_cache)
    user_input = st.text_input("Type your message here", key="user_input", on_change=set_send_input)

    voice_recording=mic_recorder(start_prompt="Start recording",stop_prompt="Stop recording", just_once=True)
    chat_container = st.container()
        


    uploaded_audio = st.sidebar.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"], key=st.session_state.audio_uploader_key)
    uploaded_image = st.sidebar.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    uploaded_pdf = st.sidebar.file_uploader("Upload a pdf file", accept_multiple_files=True, key="pdf_upload", type=["pdf"], on_change=toggle_pdf_chat)

    if uploaded_pdf:
        with st.spinner("Processing pdf..."):
            add_documents_to_db(uploaded_pdf)

    if uploaded_audio:
        transcribed_audio = transcribe_audio(uploaded_audio.getvalue())
        print(transcribed_audio)
        llm_chain = load_chain()
        llm_answer = llm_chain.run(user_input = "Summarize this text: " + transcribed_audio, chat_history=[])
        save_audio_message(get_session_key(), "human", uploaded_audio.getvalue())
        save_text_message(get_session_key(), "ai", llm_answer)
        st.session_state.audio_uploader_key += 1

    if voice_recording:
        transcribed_audio = transcribe_audio(voice_recording["bytes"])
        print(transcribed_audio)
        llm_chain = load_chain()
        llm_answer = llm_chain.run(user_input = transcribed_audio, chat_history=load_last_k_text_messages(get_session_key(), 4))
        save_audio_message(get_session_key(), "human", voice_recording["bytes"])
        save_text_message(get_session_key(), "ai", llm_answer)


    if st.session_state.send_input:
        if uploaded_image:
            with st.spinner("Processing image..."):
                llm_answer = handle_image(uploaded_image.getvalue(), st.session_state.user_question)
                save_text_message(get_session_key(), "human", st.session_state.user_question)
                save_image_message(get_session_key(), "human", uploaded_image.getvalue())
                save_text_message(get_session_key(), "ai", llm_answer)
                st.session_state.user_question = ""


        if st.session_state.user_question != "":
            llm_chain = load_chain()
            llm_answer = llm_chain.run(user_input = st.session_state.user_question, chat_history=load_last_k_text_messages(get_session_key(), 4))
            save_text_message(get_session_key(), "human", st.session_state.user_question)
            save_text_message(get_session_key(), "ai", llm_answer)
            st.session_state.user_question = ""

        st.session_state.send_input = False

    if (st.session_state.session_key != "new_session") != (st.session_state.new_session_key != None):
        with chat_container:
            #st.write("Chat History:")
            chat_history_messages = load_messages(get_session_key())

            for message in reversed(chat_history_messages):
                st.write(get_media_template(message["content"], message["message_type"], message["sender_type"]), unsafe_allow_html=True)

        if (st.session_state.session_key == "new_session") and (st.session_state.new_session_key != None):
            st.rerun()

if __name__ == "__main__":
    main()
