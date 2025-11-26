import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Photo Analyst", layout="centered")

# --- API SETUP ---
# It uses the same secret key you already set up!
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-pro")
except Exception as e:
    st.error("Please add your Google API Key to Streamlit Secrets!")
    st.stop()

# --- APP TITLE ---
st.title("📸 AI Photo Analyst")
st.write("Upload a photo and I will tell you everything about it.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Show the user their image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # 2. Create the Prompt Input
    prompt = st.text_input("Ask a question about this image (or leave blank for a summary):")

    # 3. Analyze Button
    if st.button("Analyze Image 🚀"):
        with st.spinner("Analyzing pixels..."):
            try:
                # If user didn't type anything, use a default prompt
                if not prompt:
                    prompt = "Describe this image in detail. List the main objects and the general vibe."

                # --- THE MAGIC LINE ---
                # We send BOTH the text prompt AND the image to the AI
                response = model.generate_content([prompt, image])
                
                # 4. Display Result
                st.subheader("Analysis Result:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
