"""Simple chat app using Streamlit"""

import streamlit as st
from llm import SimpleChatbot

st.title("Simple Chatbot")

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = SimpleChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your message"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display assistant response
    with st.chat_message("assistant"):
        response = st.session_state.chatbot.chat(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# Reset button in sidebar
with st.sidebar:
    if st.button("Reset conversation"):
        st.session_state.chatbot.reset()
        st.session_state.messages = []
        st.rerun()
