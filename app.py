import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mein Biograf", page_icon="📖")
st.title("Mein Biograf")

# API-Schlüssel laden
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Der API-Schlüssel fehlt noch!")
    st.stop()

# Biograf-Logik
system_instruction = """
Du bist ein persönlicher Biograf. Höre zu, sei freundlich und fasse Erlebnisse zusammen.
"""

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
    st.session_state.chat_session = model.start_chat(history=[])
    with st.chat_message("ai"):
        st.markdown("Hallo! Ich bin bereit. Erzähl mir was.")

for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "ai"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

user_input = st.chat_input("Erzähl mir etwas...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    try:
        response = st.session_state.chat_session.send_message(user_input)
        with st.chat_message("ai"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Fehler: {e}")
