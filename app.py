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

# Initialize session state safely
for key in ["logged_in", "room_code", "username"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else ""

if not st.session_state.logged_in:
    with st.container():
        st.markdown("""
            <div style='background-color:#f0f2f6;padding:30px;border-radius:10px;text-align:center;'>
            <h3>Enter Room</h3>
        """, unsafe_allow_html=True)
        
        room_code = st.text_input("Room Code")
        username = st.text_input("Your Name")
        
        if st.button("Join Chat"):
            if not room_code or not username:
                st.warning("Please fill in both fields.")
            else:
                data = load_data()
                if room_code not in data:
                    data[room_code] = {"users": [], "messages": []}

                if username not in data[room_code]["users"]:
                    if len(data[room_code]["users"]) < 2:
                        data[room_code]["users"].append(username)
                        save_data(data)
                    else:
                        st.error("Room is full. Only 2 users allowed.")
                        st.stop()
                st.session_state.logged_in = True
                st.session_state.room_code = room_code
                st.session_state.username = username
                st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)

else:
    room_code = st.session_state.room_code
    username = st.session_state.username
    data = load_data()

    if room_code not in data:
        st.error("Room not found.")
        st.stop()

    st.success(f"Logged in as {username} in room: {room_code}")

    st.markdown("---")
    st.subheader("Chat Messages")

    chat_box = st.empty()
    with chat_box:
        for msg in data[room_code]["messages"][-50:]:
            st.markdown(
                f"<div style='padding:5px;margin-bottom:8px;'>"
                f"<b>{msg['user']}</b> <span style='color:gray;font-size:12px;'>[{msg['time']}]</span><br>"
                f"{msg['message']}</div>",
                unsafe_allow_html=True
            )

    message = st.text_input("Type your message", key="message_input")
    if st.button("Send"):
        if message.strip():
            timestamp = datetime.now().strftime("%H:%M")
            data[room_code]["messages"].append({
                "user": username,
                "message": message.strip(),
                "time": timestamp
            })
            save_data(data)
            st.experimental_rerun()

    if st.button("Leave Room"):
        st.session_state.logged_in = False
        st.session_state.room_code = ""
        st.session_state.username = ""
        st.experimental_rerun()
