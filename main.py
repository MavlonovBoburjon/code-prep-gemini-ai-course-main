import os

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_response,
                            gemini_pro_vision_response,
                            embeddings_model_response)


working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('Deep Gemini AI',
                           ['ChatBot',
                            'Suratga Izoh',
                            'Matnni joylashtirish',
                            'Biror narsa so\'rang'],
                           menu_icon='robot',
                           icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                           default_index=0
                           )


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:  # Renamed for clarity
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Deep Geminidan so'rang...")  # Renamed for clarity
    try:
        if user_prompt:
            # Add user's message to chat and display it
            st.chat_message("user").markdown(user_prompt)

            # Send user's message to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(user_prompt)  # Renamed for clarity

            # Display Gemini-Pro's response
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
    except Exception as e: st.error('Tizimda xatolik bor birozdan so\'ng urinib ko\'ring', icon="🚨")


# Image captioning page
if selected == "Suratga Izoh":

    st.title("📷 Snap Kamera")

    uploaded_image = st.file_uploader("Surat Yuklang...", type=["jpg", "jpeg", "png"])

    if st.button("Rasmni generatsiya qilish"):
        try:
            image = Image.open(uploaded_image)

            col1, col2 = st.columns(2)

            with col1:
                resized_img = image.resize((800, 500))
                st.image(resized_img)

            default_prompt = "Manashu rasmga qisqacha izoh yozib bering"  # change this prompt as per your requirement

            # get the caption of the image from the gemini-pro-vision LLM
            caption = gemini_pro_vision_response(default_prompt, image)

            with col2:
                st.info(caption)
        except Exception as e: st.error('Tizimda xatolik bor birozdan so\'ng urinib ko\'ring', icon="🚨")


# text embedding model
if selected == "Matnni joylashtirish":

    st.title("🔡 Matn joylashtiring")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="O'rnatishlarni olish uchun matnni kiriting")

    try:
        if st.button("Javob olish"):
            response = embeddings_model_response(user_prompt)
            st.markdown(response)
    except Exception as e: st.error('Tizimda xatolik bor birozdan so\'ng urinib ko\'ring', icon="🚨")


# text embedding model
if selected == "Biror narsa so\'rang":

    st.title("❓ Menga savol bering")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Biror narsa so\'rang...")

    try:
        if st.button("Javob olish"):
            response = gemini_pro_response(user_prompt)
            st.markdown(response)
    except Exception as e: st.error('Tizimda xatolik bor birozdan so\'ng urinib ko\'ring', icon="🚨")