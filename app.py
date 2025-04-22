import streamlit as st
import streamlit.components.v1 as components

st.title("Peer-to-Peer Video Chat Room")

room_code = st.text_input("Enter Room Code", max_chars=10)

if room_code:
    st.success(f"Joined room: {room_code}")
    
    # Embed the HTML + JS for PeerJS-based video chat
    components.html(f"""
    <html>
    <head>
        <script src="https://unpkg.com/peerjs@1.4.7/dist/peerjs.min.js"></script>
    </head>
    <body>
        <video id="local-video" autoplay muted playsinline style="width: 45%; border: 2px solid green;"></video>
        <video id="remote-video" autoplay playsinline style="width: 45%; border: 2px solid blue;"></video>

        <script>
            const room = "{room_code}";
            const peer = new Peer(room, {{
                host: 'peerjs-server.herokuapp.com',
                secure: true,
                port: 443
            }});

            navigator.mediaDevices.getUserMedia({{ video: true, audio: true }})
            .then(stream => {{
                document.getElementById('local-video').srcObject = stream;

                peer.on('call', call => {{
                    call.answer(stream);
                    call.on('stream', remoteStream => {{
                        document.getElementById('remote-video').srcObject = remoteStream;
                    }});
                }});

                peer.on('open', id => {{
                    if (id !== room) {{
                        const call = peer.call(room, stream);
                        call.on('stream', remoteStream => {{
                            document.getElementById('remote-video').srcObject = remoteStream;
                        }});
                    }}
                }});
            }})
            .catch(error => {{
                alert("Camera/Microphone access denied.");
            }});
        </script>
    </body>
    </html>
    """, height=500)
