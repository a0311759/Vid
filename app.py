import streamlit as st
import json
import os
import time
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

# Input section
room_code = st.text_input("Enter Room Code")
username = st.text_input("Enter Your Name")

if room_code and username:
    data = load_data()

    # Initialize room if needed
    if room_code not in data:
        data[room_code] = {"users": [], "messages": []}
        save_data(data)

    # Register user
    if username not in data[room_code]["users"]:
        if len(data[room_code]["users"]) < 2:
            data[room_code]["users"].append(username)
            save_data(data)
        else:
            st.warning("Room is full (only 2 users allowed).")

    if username in data[room_code]["users"]:
        st.success(f"You joined room: {room_code}")

        # Message input
        message = st.text_input("Type your message", key="msg")

        if st.button("Send"):
            if message.strip():
                timestamp = datetime.now().strftime("%H:%M")
                data = load_data()  # reload before update
                data[room_code]["messages"].append({
                    "user": username,
                    "message": message,
                    "time": timestamp
                })
                save_data(data)
                st.experimental_rerun()

        st.subheader("Chat Messages:")

        chat_box = st.empty()

        # Auto-refresh loop for chat display
        for _ in range(200):  # refresh every 1s for ~3 mins
            data = load_data()
            messages = data[room_code]["messages"]
            with chat_box.container():
                for msg in messages:
                    st.markdown(f"**{msg['user']}** [{msg['time']}]: {msg['message']}")
            time.sleep(1)
            st.experimental_rerun()  # refresh page to show new messages
    else:
        st.info("Waiting for a slot to join...")
else:
    st.info("Enter room code and your name to join.")
        
