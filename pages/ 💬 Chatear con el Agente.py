from time import sleep

import streamlit as st
from streamlit_server_state import server_state, server_state_lock

from model import ExpertAgent
from utils.acknowledge import show_creator_acknowledgement
from utils.pwd import check_password

# Set up Session State
if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None

if "ExpertAgentInstructions" not in st.session_state:
    st.session_state["ExpertAgentInstructions"] = ""

if "ExpertAgentTemperature" not in st.session_state:
    st.session_state["ExpertAgentTemperature"] = None

if "DocumentUploader" not in st.session_state:
    st.session_state["DocumentUploader"] = None

if "index_name" not in st.session_state:
    st.session_state["index_name"] = None

with server_state_lock["documents"]:
    if "documents" not in server_state:
        server_state.documents = []


st.title("Chat con el Agente Experto")
if not check_password():
    st.stop()  # Do not continue if check_password is not True.


st.sidebar.title("Ajustes del Chat")

with st.sidebar:
    # Reset Memory
    st.markdown(
        "Si quieres empezar una nueva conversación, puedes borrar su memoria, pero mantener su descripción"
    )
    if st.button("Borrar memoria del agente"):
        if st.session_state.ExpertAgent:
            try:
                st.session_state.ExpertAgent.chat_history = (
                    st.session_state.ExpertAgent.chat_history[:1]
                )
                reset_banner = st.success("Memoria borrada")
                sleep(0.5)
                reset_banner.empty()

            except Exception as e:
                st.error(f"La memoria no ha sido reseteada:\n {e}", icon="🧠")
        else:
            st.error("La memoria no se puede resetear porque no has creado un Agente")
# Prints the whole convo
if isinstance(st.session_state.ExpertAgent, ExpertAgent):
    if st.session_state.ExpertAgent.chat_history:
        for message in st.session_state.ExpertAgent.chat_history[2:]:
            if message.type == "human":
                with st.chat_message(message.content, avatar="👨"):
                    st.markdown(message.content)
            else:
                with st.chat_message(message.content, avatar="🤖"):
                    st.markdown(message.content)

    user_input = st.chat_input("Escribe aquí tu consulta al agente experto")

    if user_input:
        with st.chat_message("user", avatar="👨"):
            st.markdown(user_input)

        # Show a typing indicator while the agent is processing the input
        with st.chat_message("Agente Experto", avatar="🤖"):

            with st.spinner("Generando Respuesta"):
                st.session_state.ExpertAgent.chat(user_input)
                ai_message = st.session_state.ExpertAgent.ai_message.content

        with st.chat_message("Agente Experto", avatar="🤖"):
            st.markdown(ai_message)
            st.rerun()

else:
    st.warning("No has creado el Agente. Ve a la configuración y pulsa en **Generar**")
