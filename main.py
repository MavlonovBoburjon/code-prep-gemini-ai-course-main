import os

from googletrans import Translator
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
footer= """<style>
a:link , a:visited{
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Mavlonov Boburjon tomonidan ishlab chiqilgan ❤ </p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu('Deep Gemini AI',
                           ['ChatBot',
                            'Matnni joylashtirish',
                            'Biror narsa so\'rang'],
                           menu_icon='robot',
                           icons=['chat-dots-fill', 'textarea-t', 'patch-question-fill'],
                           default_index=0
                           )


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, src='uz', dest='en')
    return translation.text

def translate_to_uzbek(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='uz')
    return translation.text
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
    print(user_prompt)
    try:
        if user_prompt:
            # Add user's message to chat and display it
            st.chat_message("user").markdown(user_prompt)

            # Send user's message to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(translate_to_english(user_prompt))  # Renamed for clarity

            # Display Gemini-Pro's response
            with st.chat_message("assistant"):
                translated_response = translate_to_uzbek(gemini_response.text)
                st.markdown(translated_response)
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
            translated_prompt = translate_to_english(user_prompt)
            response = gemini_pro_response(translated_prompt)
            translated_response = translate_to_uzbek(response)
            st.markdown(translated_response)
    except Exception as e: st.error('Tizimda xatolik bor birozdan so\'ng urinib ko\'ring', icon="🚨")
