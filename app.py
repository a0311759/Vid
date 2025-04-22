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

# Enter room code and username
room_code = st.text_input("Enter Room Code")
username = st.text_input("Enter Your Name")

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

    # Only allow if user is part of room
    if username in data[room_code]["users"]:
        st.success(f"You joined room: {room_code}")
        message = st.text_input("Type your message", key="msg")

        if st.button("Send"):
            if message.strip():
                timestamp = datetime.now().strftime("%H:%M")
                data[room_code]["messages"].append({
                    "user": username,
                    "message": message,
                    "time": timestamp
                })
                save_data(data)

        # Refresh button
        if st.button("Refresh Messages"):
            st.experimental_rerun()

        st.subheader("Chat Messages:")
        messages = data[room_code]["messages"]
        for msg in messages:
            sender = msg["user"]
            time = msg["time"]
            text = msg["message"]
            st.markdown(f"**{sender}** [{time}]: {text}")
    else:
        st.info("Waiting for a slot to join...")
else:
    st.info("Enter room code and your name to join.")
    
