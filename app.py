import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "chat_data.json"

# Load/initialize chat data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

st.set_page_config(page_title="Chat Room", layout="wide")
st.markdown("<style> .block-container { padding: 2rem 1rem; } </style>", unsafe_allow_html=True)

# Session states
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'room_code' not in st.session_state:
    st.session_state.room_code = ''
if 'username' not in st.session_state:
    st.session_state.username = ''

# Overlay login screen
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: #f0f2f6;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="overlay">', unsafe_allow_html=True)
        st.title("Join Chat Room")
        room = st.text_input("Room Code", key="room")
        user = st.text_input("Your Name", key="user")
        if st.button("Join"):
            if room and user:
                data = load_data()
                if room not in data:
                    data[room] = {"users": [], "messages": []}
                if user not in data[room]["users"]:
                    if len(data[room]["users"]) < 2:
                        data[room]["users"].append(user)
                        save_data(data)
                        st.session_state.logged_in = True
                        st.session_state.room_code = room
                        st.session_state.username = user
                    else:
                        st.warning("Room is full.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.room_code = room
                    st.session_state.username = user
        st.markdown('</div>', unsafe_allow_html=True)

# If logged in, show chat room
if st.session_state.logged_in:
    room_code = st.session_state.room_code
    username = st.session_state.username
    data = load_data()

    st.markdown(f"<h3>Room: {room_code} | User: {username}</h3>", unsafe_allow_html=True)

    # Chat messages area
    chat_area = st.empty()
    with chat_area.container():
        st.markdown('<div style="height:400px; overflow-y:scroll; padding:10px; border:1px solid #ccc; border-radius:10px;">', unsafe_allow_html=True)
        messages = data[room_code]["messages"]
        for msg in messages:
            sender = msg["user"]
            time = msg["time"]
            text = msg["message"]
            align = "right" if sender == username else "left"
            bg = "#dcf8c6" if sender == username else "#fff"
            st.markdown(f'''
                <div style="text-align: {align}; margin: 5px;">
                    <div style="display: inline-block; background: {bg}; padding: 8px 12px; border-radius: 10px;">
                        <strong>{sender}</strong> <span style="font-size: 10px;">[{time}]</span><br>{text}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input at bottom
    st.markdown("---")
    col1, col2 = st.columns([8, 2])
    with col1:
        message = st.text_input("Type your message...", key="chat_input", label_visibility="collapsed")
    with col2:
        if st.button("Send"):
            if message.strip():
                timestamp = datetime.now().strftime("%H:%M")
                data[room_code]["messages"].append({
                    "user": username,
                    "message": message,
                    "time": timestamp
                })
                save_data(data)
                st.experimental_rerun()
                
