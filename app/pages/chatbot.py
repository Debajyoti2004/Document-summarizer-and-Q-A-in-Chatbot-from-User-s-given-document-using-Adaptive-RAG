import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from graph import compile_workflow

st.set_page_config(page_title="Chatbot", layout="centered")
st.title("Chatbot")

app = compile_workflow()

st.subheader("Chat with your uploaded documents")
user_query = st.text_input("Enter your question:", placeholder="Ask something...")

ask_button = st.button("Ask", key="ask_button")

if ask_button and user_query.strip():
    response = app.invoke({"question": user_query})
    st.write("**Chatbot:**", response)
elif ask_button:
    st.warning("Please enter a valid question.")
