import streamlit as st
import requests

# Change this accordingly if deployed on EC2/GCP/Azure later
BACKEND_URL = "https://medicalchatbot-m3p5.onrender.com"

st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🩺",
)

st.title("🩺 Medical Chatbot Assistant")
st.write("Ask medical questions and get responses based on RAG pipeline.")

# Chat session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Ask for user input
prompt = st.chat_input("Ask a medical question...")

if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Send request to your Flask backend
    try:
        with st.spinner("Generating answer..."):
            res = requests.post(
                BACKEND_URL,
                json={"query": prompt}
            )
            data = res.json()
            response_text = data.get("answer", "No response received.")

        # Display response
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        with st.chat_message("assistant"):
            st.write(response_text)

    except Exception as e:
        st.error(f"Error communicating with backend: {e}")
