import streamlit as st
import pandas as pd

# --- App Title ---
st.title("📊 My First Streamlit App")
st.write("This is my Beast Mode Day 1 demo app 🚀")

# --- Load Sample Data ---
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df = pd.read_csv(url)

# --- Display Data ---
st.subheader("Dataset Preview")
st.dataframe(df.head())

# --- Simple Stats ---
st.subheader("Summary Statistics")
st.write(df.describe())

# --- Visualization ---
st.subheader("Total Bill Distribution")
st.bar_chart(df['total_bill'])

# --- User Interaction ---
st.subheader("Filter by Day")
day = st.selectbox("Choose a day", df['day'].unique())
filtered_df = df[df['day'] == day]
st.write(filtered_df)
