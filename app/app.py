import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000/chat"  # adjust if backend runs elsewhere

st.set_page_config(page_title="Pre-consultation Chatbot", page_icon="🍐")
st.title("🍐 pEAR: Psychological Pre-consultation Chatbot")

st.info(
    "Hello! I am pEAR, a pre-consultation assistant, here to lend you a listening ear!"
    " Please note that I cannot diagnose, treat, or provide medical advice."
    " If you are in crisis, please contact a medical professional or emergency services."
)

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": "...", "content": "..."}

# Render history
for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.write(turn["content"])

# Send message to backend
def send_message(user_text: str) -> str:
    try:
        resp = requests.post(BACKEND_URL, json={"message": user_text}, timeout=60)
        resp.raise_for_status()
        return resp.json().get("response", "[No response]")
    except Exception as e:
        return f"[Error contacting backend: {e}]"

# Chat input
user_input = st.chat_input("Type your message")

if user_input:
    # Show user message
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get assistant reply
    reply = send_message(user_input)
    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

# AI Disclaimer at the bottom - code made with reference to Copilot prompt
st.markdown(
    """
    <div style='
        position: fixed;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        max-width: 1200px;
        min-width: 400px;
        background: #d7e8fa;
        color: #1a237e;
        border-radius: 20px 20px 0 0;
        border: 1px solid #ffe58f;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        padding: 10px 10px;
        margin-bottom: 8px;
        text-align: center;
        z-index: 100;
    '>
        ⚠️ As an AI, pEAR is not a substitute for professional help. Its main purpose is to provide emotional support.
    </div>
    """,
    unsafe_allow_html=True
)
