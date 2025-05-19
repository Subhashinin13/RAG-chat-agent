import streamlit as st
import requests

st.title("RAG Chat Agent - Federal Register")

query = st.text_input("Ask a question:")

if query:
    with st.spinner("Thinking..."):
        response = requests.post("http://127.0.0.1:8000/chat", json={"user_query": query})
        if response.status_code == 200:
            st.markdown("**Agent:** " + response.json()["response"])
        else:
            st.error("Something went wrong.")
