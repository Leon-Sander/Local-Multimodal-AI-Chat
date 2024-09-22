# Local Multimodal AI Chat - Multimodal chat application with local models
# Copyright (C) 2024 Leon Sander
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import streamlit as st
from chat_api_handler import ChatAPIHandler
from streamlit_mic_recorder import mic_recorder
from utils import get_timestamp, load_config, get_avatar
from audio_handler import transcribe_audio
from pdf_handler import add_documents_to_db
from html_templates import css
from database_operations import save_text_message, save_image_message, save_audio_message, load_messages, get_all_chat_history_ids, delete_chat_history, load_last_k_text_messages_ollama
from utils import list_openai_models, list_ollama_models, command
import sqlite3
config = load_config()

def toggle_pdf_chat():
    st.session_state.pdf_chat = True
    clear_cache()

def detoggle_pdf_chat():
    st.session_state.pdf_chat = False

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

def list_model_options():
    if st.session_state.endpoint_to_use == "ollama":
        ollama_options = list_ollama_models()
        if ollama_options == []:
            #save_text_message(get_session_key(), "assistant", "No models available, please choose one from https://ollama.com/library and pull with /pull <model_name>")
            st.warning("No ollama models available, please choose one from https://ollama.com/library and pull with /pull <model_name>")
        return ollama_options
    elif st.session_state.endpoint_to_use == "openai":
        return list_openai_models()

def update_model_options():
    st.session_state.model_options = list_model_options()

def main():
    st.title("Multimodal Local Chat App")
    st.write(css, unsafe_allow_html=True)
    
    if "db_conn" not in st.session_state:
        st.session_state.session_key = "new_session"
        st.session_state.new_session_key = None
        st.session_state.session_index_tracker = "new_session"
        st.session_state.db_conn = sqlite3.connect(config["chat_sessions_database_path"], check_same_thread=False)
        st.session_state.audio_uploader_key = 0
        st.session_state.pdf_uploader_key = 1
        st.session_state.endpoint_to_use = "ollama"
        st.session_state.model_options = list_model_options()
        st.session_state.model_tracker = None
    if st.session_state.session_key == "new_session" and st.session_state.new_session_key != None:
        st.session_state.session_index_tracker = st.session_state.new_session_key
        st.session_state.new_session_key = None

    st.sidebar.title("Chat Sessions")
    chat_sessions = ["new_session"] + get_all_chat_history_ids()
    try:
        index = chat_sessions.index(st.session_state.session_index_tracker)
    except ValueError:
        st.session_state.session_index_tracker = "new_session"
        index = chat_sessions.index(st.session_state.session_index_tracker)
        clear_cache()

    st.sidebar.selectbox("Select a chat session", chat_sessions, key="session_key", index=index)
    api_col, model_col = st.sidebar.columns(2)
    api_col.selectbox(label="Select an API", options = ["ollama","openai"], key="endpoint_to_use", on_change=update_model_options)
    model_col.selectbox(label="Select a Model", options = st.session_state.model_options, key="model_to_use")
    pdf_toggle_col, voice_rec_col = st.sidebar.columns(2)
    pdf_toggle_col.toggle("PDF Chat", key="pdf_chat", value=False, on_change=clear_cache)
    with voice_rec_col:
        voice_recording=mic_recorder(start_prompt="Record Audio",stop_prompt="Stop recording", just_once=True)
    delete_chat_col, clear_cache_col = st.sidebar.columns(2)
    delete_chat_col.button("Delete Chat Session", on_click=delete_chat_session_history)
    #clear_cache_col.button("Clear Cache", on_click=clear_cache)
    
    chat_container = st.container()
    user_input = st.chat_input("Type your message here", key="user_input")
    
    uploaded_pdf = st.sidebar.file_uploader("Upload a pdf file", accept_multiple_files=True, 
                                        key=st.session_state.pdf_uploader_key, type=["pdf"], on_change=toggle_pdf_chat)
    uploaded_image = st.sidebar.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"], on_change=detoggle_pdf_chat)
    uploaded_audio = st.sidebar.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"], key=st.session_state.audio_uploader_key)

    if uploaded_pdf:
        with st.spinner("Processing pdf..."):
            add_documents_to_db(uploaded_pdf)
            st.session_state.pdf_uploader_key += 2

    if voice_recording:
        transcribed_audio = transcribe_audio(voice_recording["bytes"])
        print(transcribed_audio)
        #llm_chain = load_chain()
        llm_answer = ChatAPIHandler.chat(user_input = transcribed_audio, 
                                   chat_history=load_last_k_text_messages_ollama(get_session_key(), config["chat_config"]["chat_memory_length"]))
        save_audio_message(get_session_key(), "user", voice_recording["bytes"])
        save_text_message(get_session_key(), "assistant", llm_answer)

    
    if user_input:
        if user_input.startswith("/"):
            response = command(user_input)
            save_text_message(get_session_key(), "user", user_input)
            save_text_message(get_session_key(), "assistant", response)
            user_input = None

        if uploaded_image:
            with st.spinner("Processing image..."):
                llm_answer = ChatAPIHandler.chat(user_input = user_input, chat_history = [], image = uploaded_image.getvalue())
                save_text_message(get_session_key(), "user", user_input)
                save_image_message(get_session_key(), "user", uploaded_image.getvalue())
                save_text_message(get_session_key(), "assistant", llm_answer)
                user_input = None

        if uploaded_audio:
            transcribed_audio = transcribe_audio(uploaded_audio.getvalue())
            print(transcribed_audio)
            llm_answer = ChatAPIHandler.chat(user_input = user_input + "\n" + transcribed_audio, chat_history=[])
            save_text_message(get_session_key(), "user", user_input)
            save_audio_message(get_session_key(), "user", uploaded_audio.getvalue())
            save_text_message(get_session_key(), "assistant", llm_answer)
            st.session_state.audio_uploader_key += 2
            user_input = None

        if user_input:
            llm_answer = ChatAPIHandler.chat(user_input = user_input, 
                                       chat_history=load_last_k_text_messages_ollama(get_session_key(), config["chat_config"]["chat_memory_length"]))
            save_text_message(get_session_key(), "user", user_input)
            save_text_message(get_session_key(), "assistant", llm_answer)
            user_input = None


    if (st.session_state.session_key != "new_session") != (st.session_state.new_session_key != None):
        with chat_container:
            chat_history_messages = load_messages(get_session_key())

            for message in chat_history_messages:
                with st.chat_message(name=message["sender_type"], avatar=get_avatar(message["sender_type"])):
                    if message["message_type"] == "text":
                        st.write(message["content"])
                    if message["message_type"] == "image":
                        st.image(message["content"])
                    if message["message_type"] == "audio":
                        st.audio(message["content"], format="audio/wav")

        if (st.session_state.session_key == "new_session") and (st.session_state.new_session_key != None):
            st.rerun()

if __name__ == "__main__":
    main()
