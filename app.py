import os
import requests
import streamlit as st
from fpdf import FPDF

# ---------------- Configuration ------------------
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL = "llama3-70b-8192"
SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop")  # Change if needed
# -------------------------------------------------

def call_groq(topic):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": "You are a helpful research assistant."},
        {"role": "user", "content": f"Write a well-structured, academic research article on: {topic}"}
    ]
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

def save_to_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    filepath = os.path.join(SAVE_FOLDER, filename)
    pdf.output(filepath)
    return filepath

# ---------------- Streamlit UI ------------------
st.set_page_config(page_title="Topic Research Agent", layout="centered")
st.title("AI Topic Research Agent")
st.markdown("Enter a topic and get a researched PDF directly on your Desktop!")

topic = st.text_input("Enter your research topic here")

if st.button("Generate PDF"):
    if topic.strip() == "":
        st.warning("Please enter a valid topic.")
    else:
        with st.spinner("Researching... Please wait"):
            try:
                report = call_groq(topic)
                filename = f"Research_on_{'_'.join(topic.title().split())}.pdf"
                filepath = save_to_pdf(report, filename)
                st.success(f"PDF saved on Desktop as: {filename}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")