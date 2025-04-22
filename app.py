import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "chat_data.json"

# Initialize JSON file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize session state safely
if "room_joined" not in st.session_state:
    st.session_state["room_joined"] = False
if "room_code" not in st.session_state:
    st.session_state["room_code"] = ""
if "username" not in st.session_state:
    st.session_state["username"] = ""

st.title("Simple Chat Room")

# Before joining
if not st.session_state["room_joined"]:
    room_code = st.text_input("Enter Room Code")
    username = st.text_input("Enter Your Name")

    if st.button("Join Room"):
        if room_code and username:
            data = load_data()

            # Create room if it doesn't exist
            if room_code not in data:
                data[room_code] = {
                    "users": [],
                    "messages": []
                }

            # Check if user can join
            if username not in data[room_code]["users"]:
                if len(data[room_code]["users"]) < 2:
                    data[room_code]["users"].append(username)
                    save_data(data)
                else:
                    st.warning("Room is full (only 2 users allowed).")
                    st.stop()

            # Join success
            st.session_state["room_joined"] = True
            st.session_state["room_code"] = room_code
            st.session_state["username"] = username
            st.experimental_rerun()

else:
    # After joining
    room = st.session_state["room_code"]
    username = st.session_state["username"]
    st.success(f"You joined room: {room} as {username}")

    data = load_data()

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
    for msg in data[room]["messages"]:
        st.markdown(f"**{msg['user']}** [{msg['time']}]: {msg['message']}")

    if st.button("Leave Room"):
        if username in data[room]["users"]:
            data[room]["users"].remove(username)
            save_data(data)
        st.session_state["room_joined"] = False
        st.session_state["room_code"] = ""
        st.session_state["username"] = ""
        st.experimental_rerun()
