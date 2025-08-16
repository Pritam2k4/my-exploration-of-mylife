# 📧 Email Spam Classifier

This project is a **Machine Learning model** that classifies emails/messages as **Spam** or **Ham** using **Naive Bayes** and **TF-IDF Vectorization**.

## 🚀 How it works
- **Preprocessing:** Text cleaning (lowercasing, punctuation removal, stopword removal)
- **Feature Extraction:** TF-IDF
- **Model:** Multinomial Naive Bayes
- **Deployment:** Streamlit Web App

## 📂 Run the Project
1. Install dependencies:
   pip install -r requirements.txt
2. Train the model (if needed) by running:
   python notebooks/preprocessing.ipynb
3. Start Streamlit:
   streamlit run app.py
