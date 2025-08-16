import streamlit as st
import pickle

# Load vectorizer and model
with open("email_spam_classifier/models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("email_spam_classifier/models/spam_model.pkl", "rb") as f:
    model = pickle.load(f)

# Title
st.title("📧 Email Spam Classifier")
st.write("Enter an email/message below to check if it's spam or not.")

# Input
user_input = st.text_area("✏️ Message:", "")

if st.button("🔍 Predict"):
    if user_input.strip() != "":
        input_vector = vectorizer.transform([user_input])
        prediction = model.predict(input_vector)[0]
        prediction_proba = model.predict_proba(input_vector)[0]

        if prediction == "spam":
            st.error(f"🚨 This message is **SPAM**! (Confidence: {prediction_proba[1]:.2f})")
        else:
            st.success(f"✅ This message is **HAM** (not spam). (Confidence: {prediction_proba[0]:.2f})")
    else:
        st.warning("⚠️ Please enter a message to classify.")
