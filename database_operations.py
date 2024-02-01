from utils import load_config
import streamlit as st
import sqlite3


def get_db_connection(db_path):
    if 'db_conn' not in st.session_state or st.session_state.db_conn is None:
        st.session_state.db_conn = sqlite3.connect(db_path, check_same_thread=False)
    return st.session_state.db_conn

def close_db_connection():
    if 'db_conn' in st.session_state and st.session_state.db_conn is not None:
        st.session_state.db_conn.close()
        st.session_state.db_conn = None


def save_text_message(db_path, chat_history_id, sender_type, text):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (chat_history_id, sender_type, message_type, text_content) VALUES (?, ?, ?, ?)',
                   (chat_history_id, sender_type, 'text', text))

    conn.commit()
    conn.close()

def save_image_message(db_path, chat_history_id, sender_type, image_bytes):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (chat_history_id, sender_type, message_type, blob_content) VALUES (?, ?, ?, ?)',
                   (chat_history_id, sender_type, 'image', sqlite3.Binary(image_bytes)))

    conn.commit()
    conn.close()

def save_audio_message(db_path, chat_history_id, sender_type, audio_bytes):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (chat_history_id, sender_type, message_type, blob_content) VALUES (?, ?, ?, ?)',
                   (chat_history_id, sender_type, 'audio', sqlite3.Binary(audio_bytes)))

    conn.commit()
    conn.close()

def load_messages(db_path, chat_history_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT message_id, sender_type, message_type, text_content, blob_content FROM messages WHERE chat_history_id = ?"
    cursor.execute(query, (chat_history_id,))

    messages = cursor.fetchall()
    chat_history = []
    for message in messages:
        message_id, sender_type, message_type, text_content, blob_content = message

        if message_type == 'text':
            chat_history.append({'message_id': message_id, 'sender_type': sender_type, 'message_type': message_type, 'content': text_content})
        else:
            chat_history.append({'message_id': message_id, 'sender_type': sender_type, 'message_type': message_type, 'content': blob_content})

    conn.close()

    return chat_history

if __name__ == "__main__":
    config = load_config()
    db_path = config["chat_sessions_database_path"]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    create_messages_table = """
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_history_id TEXT NOT NULL,
        sender_type TEXT NOT NULL,
        message_type TEXT NOT NULL,
        text_content TEXT,
        blob_content BLOB
    );
    """

    cursor.execute(create_messages_table)
    conn.commit()
    conn.close()