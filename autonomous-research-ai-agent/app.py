import streamlit as st
from src.agent import run_query

st.set_page_config(
    page_title="Autonomous Research AI Agent",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Autonomous Research AI Agent")
st.caption("Powered by Groq + DuckDuckGo | Built with LangChain")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask me anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            response = run_query(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})