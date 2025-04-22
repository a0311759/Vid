import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import uuid

# App title
st.title("Private Video Chat Room")

# Room code input
st.subheader("Join or Create a Room")
room_code = st.text_input("Enter Room Code:", value="", max_chars=10)

if not room_code:
    st.warning("Please enter a room code to join.")
else:
    st.success(f"You're in room: {room_code}")

    # Use room code to set a shared signaling namespace
    webrtc_streamer(
        key=room_code,
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={  # For basic STUN servers
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
        media_stream_constraints={"video": True, "audio": True},
    )
