import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.chat_engine import get_engine 

st.set_page_config(page_title="Pre-consultation Chatbot", page_icon="🍐")
st.title("🍐 pEAR: Psychological Pre-consultation Chatbot")

st.info(
    "Hello! I am pEAR , a pre-consultation assistant, here to lend you a listening ear!"
    " Please note that I cannot diagnose, treat, or provide medical advice."
    " If you are in crisis, please contact a medical professional or emergency services."
)

# Get the chat engine instance
engine = get_engine()

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = engine.conversation_history.copy() # list of {"role": "...", "content": "..."}
if "loading" not in st.session_state:
    st.session_state.loading = False
if "engine" not in st.session_state:
    st.session_state.engine = get_engine()

safety_indicators = {
    "allow": {"color": "#C5DEA9", "indicator": "💬"},
    "safe_fallback": {"color": "#FDEBC8", "indicator": "⚠️"},
    "block": {"color": "#E89464", "indicator": "⛔"},
}

# Render history - made with copilot prompt
# Prompt: how to keep the colour for previous messages? 
# my current code has the indicator for the latest response, but previous responses 
# lose their indicators
for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        if turn["role"] == "assistant":
            indicator = safety_indicators.get(turn.get("safety_action", "allow"), safety_indicators["allow"]) # default to allow
            color = indicator["color"]
            icon = indicator["indicator"]
            st.markdown(
                f"""
                <div style='background:{color}; color:#000000; padding:12px; border-radius:12px; display:flex; flex-direction:column; align-items:left;'>
                    <span style='font-size:1em; margin-bottom:3px;'>{icon}</span>
                    <span>{turn['content']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write(turn["content"])

# Chat input
if user_input := st.chat_input("Type your message here..."):
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get assistant reply
    result = engine.process_message(user_input)
    reply = result.get("response", "[No response]")
    safety_action = result.get("safety_action", "allow")  # Use "allow" as default
    st.session_state.history.append({"role": "assistant", "content": reply, "safety_action": safety_action})

    with st.chat_message("assistant"):
        indicator = safety_indicators.get(safety_action, safety_indicators["allow"])
        color = indicator["color"]
        icon = indicator["indicator"]
        st.markdown(
            f"""
            <div style='background:{color}; color:#000000; padding:12px; border-radius:12px; display:flex; flex-direction:column; align-items:left;'>
                <span style='font-size:1em; margin-bottom:3px;'>{icon}</span>
                <span>{reply}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

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
        ⚠️ As an AI, pEAR is not a substitute for professional help.
    </div>
    """,
    unsafe_allow_html=True
)
