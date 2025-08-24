import streamlit as st
import time
from chatbot import HiringAssistant

st.set_page_config(page_title="TalentScout Assistant", page_icon="🤖", layout="centered")

# CSS for chat style with dynamic width
st.markdown("""
<style>
.chat-message {
    display: inline-block; /* Box width fits content */
    border-radius: 12px;
    padding: 12px 18px;
    margin: 10px 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    transition: all 0.3s ease-in-out;
    max-width: 80%; /* Prevents overly wide messages */
    word-wrap: break-word; /* Wrap long words */
}

/* User messages */
.user-message {
    background: linear-gradient(135deg, #3a7bd5, #00d2ff);
    color: white;
    margin-left: auto;
    text-align: right;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

/* Assistant messages */
.assistant-message {
    background: #f7f7f8;
    color: #222;
    margin-right: auto;
    text-align: left;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
.chat-message {
    animation: fadeIn 0.3s ease-in-out;
}

.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding-right: 10px;
}
</style>
""", unsafe_allow_html=True)

# Page title
st.markdown("## TalentScout - Hiring Assistant")
st.markdown("Welcome! I will guide you through a professional **initial screening process** with structured, clear responses.")

# Initialize assistant
if "assistant" not in st.session_state:
    st.session_state.assistant = HiringAssistant()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function for animated typing effect
def type_text(message, delay=0.02):
    placeholder = st.empty()
    displayed_text = ""
    for char in message:
        displayed_text += char
        # Use div without max-width restriction (handled by CSS)
        placeholder.markdown(f'<div class="chat-message assistant-message">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(delay)
    return placeholder

# Display previous messages
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">{chat["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message">{chat["message"]}</div>', unsafe_allow_html=True)

# Get user input
user_input = st.chat_input("Type your response here...")

if user_input:
    # Show user message
    st.markdown(f'<div class="chat-message user-message">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "message": user_input})

    # Get assistant reply
    reply = st.session_state.assistant.chat(user_input)

    # Animate assistant typing
    type_text(reply)

    # Save assistant message in history
    st.session_state.chat_history.append({"role": "assistant", "message": reply})
