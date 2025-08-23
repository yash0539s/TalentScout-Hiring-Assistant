import streamlit as st
from chatbot import HiringAssistant

st.set_page_config(page_title="TalentScout Assistant", page_icon="🤖", layout="centered")
st.title("🤖 TalentScout - Hiring Assistant")
st.write("Welcome! I will guide you through an initial screening process.")

if "assistant" not in st.session_state:
    st.session_state.assistant = HiringAssistant()

user_input = st.chat_input("Type your response here...")

if user_input:
    reply = st.session_state.assistant.chat(user_input)
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(reply)
