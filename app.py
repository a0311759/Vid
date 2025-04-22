import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "chat_data.json"

# Create empty data file if not present
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize session state
if "room_joined" not in st.session_state:
    st.session_state["room_joined"] = False
if "room_code" not in st.session_state:
    st.session_state["room_code"] = ""
if "username" not in st.session_state:
    st.session_state["username"] = ""

st.title("Simple Chat Room")

# --- BEFORE JOINING ROOM ---
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

            # Check if room has space
            if username not in data[room_code]["users"]:
                if len(data[room_code]["users"]) < 2:
                    data[room_code]["users"].append(username)
                    save_data(data)
                else:
                    st.warning("Room is full (only 2 users allowed).")
                    st.stop()

            # Save session state
            st.session_state["room_joined"] = True
            st.session_state["room_code"] = room_code
            st.session_state["username"] = username
            st.experimental_rerun()

# --- AFTER JOINING ROOM ---
else:
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

    # --- SAFE LEAVE ROOM BUTTON ---
    if st.button("Leave Room"):
        data = load_data()
        room = st.session_state.get("room_code", "")
        username = st.session_state.get("username", "")

        if room in data:
            if "users" in data[room] and username in data[room]["users"]:
                data[room]["users"].remove(username)

                # Clean up room if empty
                if not data[room]["users"] and not data[room]["messages"]:
                    del data[room]

                save_data(data)

        # Reset session
        st.session_state["room_joined"] = False
        st.session_state["room_code"] = ""
        st.session_state["username"] = ""
        st.experimental_rerun()
