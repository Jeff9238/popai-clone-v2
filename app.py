import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# 1. Configure the API
# PASTE YOUR KEY HERE
genai.configure(api_key="AIzaSyDGPct5nq23Glez-czINM9JDUUkvbr_TkY")
model = genai.GenerativeModel("gemini-2.5-pro")

# 2. Page Setup
st.set_page_config(page_title="My PopAi Clone", layout="wide")
st.title("📄 Chat with any PDF")

# 3. Sidebar for PDF Upload
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    # Extract text from PDF if a file is uploaded
    pdf_text = ""
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text()
        st.success("PDF Loaded Successfully! ✅")

# 4. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle New Messages
if prompt := st.chat_input("Ask a question about your PDF..."):
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare the prompt for AI
    # We combine the User's Question + The PDF Content
    if pdf_text:
        full_prompt = f"Here is a document: {pdf_text}\n\nBased on this document, answer this question: {prompt}"
    else:
        full_prompt = prompt

    # Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing document..."):
            try:
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")