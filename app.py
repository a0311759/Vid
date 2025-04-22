import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "chat_data.json"

# Load and save JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Page config
st.set_page_config(page_title="Chat Room", layout="centered")
st.markdown("<h1 style='text-align:center;'>Chat Room App</h1>", unsafe_allow_html=True)

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.container():
        st.markdown("""
            <div style='background-color:#f0f2f6;padding:30px;border-radius:10px;text-align:center;'>
            <h3>Enter Room</h3>
        """, unsafe_allow_html=True)
        room_code = st.text_input("Room Code", key="room_code_input")
        username = st.text_input("Your Name", key="username_input")
        login = st.button("Join Chat")

        if login and room_code and username:
            data = load_data()
            if room_code not in data:
                data[room_code] = {
                    "users": [],
                    "messages": []
                }

            if username not in data[room_code]["users"]:
                if len(data[room_code]["users"]) < 2:
                    data[room_code]["users"].append(username)
                    save_data(data)
                    st.session_state.logged_in = True
                    st.session_state.room_code = room_code
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error("Room is full. Only 2 users allowed.")
            else:
                st.session_state.logged_in = True
                st.session_state.room_code = room_code
                st.session_state.username = username
                st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Chat UI
    room_code = st.session_state.room_code
    username = st.session_state.username
    data = load_data()

    st.success(f"Logged in as {username} in room: {room_code}")

    with st.container():
        st.markdown("---")
        st.markdown("<h4>Chat Messages</h4>", unsafe_allow_html=True)
        chat_box = st.empty()

        # Show messages
        messages = data[room_code]["messages"]
        with chat_box:
            for msg in messages[-50:]:
                sender = msg["user"]
                text = msg["message"]
                time = msg["time"]
                st.markdown(f"<div style='padding:5px;'><b>{sender}</b> <span style='color:gray;font-size:12px;'>[{time}]</span><br>{text}</div>", unsafe_allow_html=True)

    # Message input
    message = st.text_input("Type your message", key="message_input")
    if st.button("Send", key="send_button"):
        if message.strip():
            timestamp = datetime.now().strftime("%H:%M")
            data[room_code]["messages"].append({
                "user": username,
                "message": message.strip(),
                "time": timestamp
            })
            save_data(data)
            st.experimental_rerun()

    # Leave room
    if st.button("Leave Room", key="leave"):
        st.session_state.logged_in = False
        st.session_state.room_code = ""
        st.session_state.username = ""
        st.experimental_rerun()
