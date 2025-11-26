import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="My PopAi Clone", layout="wide")

# --- API SETUP (SECURE) ---
# This looks for the key in the "Secrets" vault, not in this file.
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Secrets.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    pdf_text = ""
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success("PDF Loaded Successfully! ✅")

# --- CHAT INTERFACE ---
st.title("📄 Chat with any PDF")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your PDF..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if pdf_text:
        full_prompt = f"Here is a document: {pdf_text}\n\nBased on this document, answer this question: {prompt}"
    else:
        full_prompt = prompt

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")
