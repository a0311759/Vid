import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "chat_data.json"

# Initialize JSON data file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

st.title("Simple Chat Room")

# Session state to track room and username
if "room_joined" not in st.session_state:
    st.session_state.room_joined = False
if "room_code" not in st.session_state:
    st.session_state.room_code = ""
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.room_joined:
    room_code = st.text_input("Enter Room Code")
    username = st.text_input("Enter Your Name")
    if st.button("Join Room"):
        if room_code and username:
            data = load_data()

            # Initialize room if it doesn't exist
            if room_code not in data:
                data[room_code] = {
                    "users": [],
                    "messages": []
                }

            # Add user if not already in room
            if username not in data[room_code]["users"]:
                if len(data[room_code]["users"]) < 2:
                    data[room_code]["users"].append(username)
                    save_data(data)
                else:
                    st.warning("Room is full (only 2 users allowed).")
                    st.stop()

            # Join successful
            st.session_state.room_joined = True
            st.session_state.room_code = room_code
            st.session_state.username = username
            st.experimental_rerun()
else:
    st.success(f"Room: {st.session_state.room_code} | You: {st.session_state.username}")

    data = load_data()
    room = st.session_state.room_code
    username = st.session_state.username

    message = st.text_input("Type your message", key="msg")
    if st.button("Send"):
        if message.strip():
            timestamp = datetime.now().strftime("%H:%M")
            data[room]["messages"].append({
                "user": username,
                "message": message,
                "time": timestamp
            })
            save_data(data)

    st.subheader("Chat Messages:")
    messages = data[room]["messages"]
    for msg in messages:
        st.markdown(f"**{msg['user']}** [{msg['time']}]: {msg['message']}")

    if st.button("Leave Room"):
        data[room]["users"].remove(username)
        save_data(data)
        st.session_state.room_joined = False
        st.session_state.room_code = ""
        st.session_state.username = ""
        st.experimental_rerun()
