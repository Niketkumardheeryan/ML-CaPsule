"""
Main Streamlit application file for the AI Song Recommender Chatbot.
This script initializes the Chatbot and handles the web interface interaction.
"""

import streamlit as st
from src.chatbot import Chatbot

st.set_page_config(page_title="Song Recommender Chatbot", page_icon="🎵")

st.title("🎵 AI Song Recommender Chatbot")

# Initialize Chatbot in session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Song Recommender Bot. How are you feeling today, or what kind of music are you looking for?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., I am feeling happy today..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response
    bot_response = st.session_state.chatbot.get_response(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
