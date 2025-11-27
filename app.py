import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Pro AI Analyst", layout="centered")

# --- 1. THE GATEKEEPER (Simulated Login) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def check_login():
    # In a real app, this connects to a database (Supabase)
    if st.session_state.password == "chemlite2025":
        st.session_state.logged_in = True
        del st.session_state.password  # don't store password
    else:
        st.error("Wrong password! Please subscribe to get access.")

if not st.session_state.logged_in:
    st.title("🔒 Premium AI Service")
    st.write("Please log in to access the Photo Analyst.")
    st.text_input("Password", type="password", on_change=check_login, key="password")
    st.stop() # STOP here if not logged in

# --- 2. THE PREMIUM CONTENT (Only runs if logged_in is True) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-pro")
except Exception:
    st.error("API Key missing.")
    st.stop()

st.sidebar.button("Log out", on_click=lambda: st.session_state.update({"logged_in": False}))

st.title("💎 VIP Photo Analyst")
st.success("Welcome back, VIP User!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")
    
    if st.button("Analyze"):
        with st.spinner("Processing..."):
            response = model.generate_content(["Describe this image", image])
            st.write(response.text)

