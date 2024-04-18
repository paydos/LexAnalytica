import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.switch_page_button import switch_page

from utils.acknowledge import show_creator_acknowledgement
from utils.pwd import check_password
from utils.session_state_inst import inst_states

inst_states()


st.set_page_config(
    page_title="LexAnalytica",
    page_icon="data/branded_icon.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)
import base64

file_ = open("data/bot.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<center><img src="data:image/gif;base64,{data_url}" alt="bot gif" width="100"></center>',
    unsafe_allow_html=True,
)
st.write("# Bienvenido a LexAnalytica")
st.write(
    "Para usar LexAnalytica, debes tener a mano tanto el JSON de evaluación como nuestro SETTINGS.toml, el cual contiene los prompts y otros ajustes de configuración de LexAnalytica. En **Evaluar Modelo** tienes una experiencia guiada para evaluar el asistente."
)

if not check_password():

    st.stop()  # Do not continue if check_password is not True.
st.markdown(
    """Esta es nuestra submission para la 2ª Edición del Hackathon Legaltech Comillas-Garrigues.
            Para evaluar el modelo en la competición, pulsa en **"Evaluar Modelo"**."""
)

st.markdown(
    """Si quieres saber más sobre la arquitectura, tecnologías y challenges con el prompt engineering, pulsa en **About**. 
                        Si te interesa saber como funciona, puedes entrar en **Configuración**"""
)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Evaluar 📊")
    st.write("Para la evaluación de LexAnalytica en el Hackathon.")
    if col1.button(
        "Evaluar modelo 📊",
        key="eval_model",
    ):
        switch_page("Evaluación")

with col2:
    st.subheader("Configuración ⚙️")
    st.write("Configura a LexAnalytica a medida.")
    if col2.button(
        "Configuración ⚙️",
        key="config",
    ):
        switch_page("Configuración")

with col3:
    st.subheader("Chatear 💬")
    st.write("Interactúa directamente con nuestro agente inteligente.")
    if col3.button("Chatear con el Agente 💬", key="chat"):
        switch_page("Chatear con el Agente")

col4, col5 = st.columns([1, 1])

with col4:
    st.subheader("Subir documentos 📤")
    st.write("Sube documentos para procesarlos o analizarlos.")
    if col4.button(
        "Subir documentos 📤",
        key="upload_docs",
        disabled=True,
    ):
        switch_page("Subir Documentos")

with col5:
    st.subheader("About 📘")
    st.write("Conoce más sobre nosotros y el proyecto.")
    if col5.button(
        "About 📘",
        key="about",
    ):
        switch_page("About")

show_creator_acknowledgement()
