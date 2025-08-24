import streamlit as st
from transformers import pipeline

# Load the model (you can change to any Hugging Face model)
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct")

assistant = load_model()

# Web Interface
st.set_page_config(page_title="Python Assistant", page_icon="🐍", layout="centered")
st.title("🐍 Python Assistant")
st.write("Ask me anything about Python, and I'll help you out!")

# User Input
user_input = st.text_area("Enter your Python question:")

if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question!")
    else:
        with st.spinner("Thinking..."):
            response = assistant(
                user_input,
                max_length=300,
                temperature=0.2,  # Low temp = less randomness
                top_p=0.9,
                do_sample=True
            )
        st.success("Here's the answer:")
        st.write(response[0]["generated_text"])
