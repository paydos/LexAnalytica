import time
from time import sleep

import streamlit as st
from streamlit_chat import message as st_message
from streamlit_extras.switch_page_button import switch_page

from model import ExpertAgent
from utils.pwd import check_password
from utils.session_state_inst import inst_states
from utils.st_utils import display_fusionRAG_docs

inst_states()
st.set_page_config(
    page_title="Chat",
    page_icon="data/branded_icon.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)
col1, col2 = st.columns([0.9, 0.1])
col1.title("Chat con LexAnalytica")
col2.image("data/bot.gif")
if not check_password():
    st.stop()  # Do not continue if check_password is not True.


st.sidebar.title("Ajustes del Chat")

with st.sidebar:
    # Reset Memory
    st.markdown(
        "Si quieres empezar una nueva conversación, puedes borrar su memoria, pero mantener su descripción"
    )
    if st.button("Borrar memoria del agente", disabled=True):
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

    st.sidebar.markdown(f"El modo examen está en **{st.session_state.examMode}**")
    st.sidebar.header("Lógica de ramas de búsqueda FusionRAG")
    if (
        "FusionRAG" in st.session_state.keys()
        and st.session_state.FusionRAG is not None
    ):
        if st.session_state.FusionRAG.fusionRAG_generated_queries is not None:
            for branch in st.session_state.FusionRAG.fusionRAG_generated_queries:
                st.markdown(f"- {branch}")
                time.sleep(0.5)
    else:
        st.warning("FusionRAG is not initialised")
    # Display selected settings for FusionRAG
    st.sidebar.header("Configuración seleccionada de FusionRAG")
    st.sidebar.markdown(
        f"Número de ramas: **{st.session_state.num_branches_fusionRAG or 'No establecido'}**"
    )
    st.sidebar.markdown(
        f"Resultados por rama: **{st.session_state.num_matches_per_branch or 'No establecido'}**"
    )
    st.sidebar.markdown(
        f"Temperatura: **{st.session_state.ExpertAgentTemperature or 'No establecido'}**"
    )

if st.session_state.examMode == False:

    tab1, tab2 = st.tabs(["Chat con el Agente", "Documentos del FusionRAG"])

    chatContainer = st.container(border=False, height=600)
    user_input = st.chat_input("Escribe aquí tu consulta al agente experto")

    with tab1:
        if isinstance(st.session_state.ExpertAgent, ExpertAgent):
            if st.session_state.ExpertAgent.chat_history:
                with chatContainer:
                    for message in st.session_state.ExpertAgent.chat_history[2:]:
                        if message.type == "human":
                            st_message(message.content, is_user=True)

                        else:
                            st_message(message.content, is_user=False)

                if user_input:
                    st_message(user_input, is_user=True)

                    # Show a typing indicator while the agent is processing the input

                    with st.status("Generando Respuesta", expanded=False) as status:
                        st.session_state.ExpertAgent.chat(user_input, status=status)
                        ai_message = st.session_state.ExpertAgent.ai_message.content
                        st_message(ai_message, is_user=False)
                    st.rerun()

        else:
            st.warning(
                "No has creado el Agente. Ve a la configuración y pulsa en **Generar**"
            )
    with tab2:
        if st.session_state.num_branches_fusionRAG:
            st.title("Resultados del FusionRAG")
            st.markdown(
                f"""Aquí puedes encontrar los documentos recuperador por el FusionRAG. Hay un total de **{st.session_state.num_branches_fusionRAG*st.session_state.num_matches_per_branch} documentos**"""
            )
            if st.session_state.FusionRAG:
                if st.session_state.FusionRAG.fusionRAG_query_to_results_map:

                    display_fusionRAG_docs(
                        st.session_state.FusionRAG.fusionRAG_query_to_results_map
                    )
                else:
                    st.warning(
                        "Vuelve cuando hayas preguntado. Todavía no se ha consultado la tienda de vectores."
                    )

else:  # In examMode == True
    if isinstance(st.session_state.ExpertAgent, ExpertAgent):
        statusBar = st.status(label="Preguntas")
        if st.session_state.unpackedQuestions:
            for i, question in enumerate(st.session_state.unpackedQuestions):

                st.session_state.ExpertAgent.chat(
                    question["unpacked_question"],
                    status=statusBar,
                    count=i,
                    total_count=len(st.session_state.unpackedQuestions),
                )
            st.session_state.ExpertAgent_finished = True

            st.success(
                "Todas las preguntas se han respondido. Pulsa en **continuar** para descargar el resultado"
            )
        if st.session_state.ExpertAgent_finished:

            if st.button("Continuar a la evaluación de las respuestas"):
                switch_page("Evaluación")

        if st.session_state.num_branches_fusionRAG:
            st.title("Resultados del FusionRAG")
            st.markdown(
                f"""Aquí puedes encontrar los documentos recuperador por el FusionRAG. Hay un total de **{st.session_state.num_branches_fusionRAG*st.session_state.num_matches_per_branch} documentos**"""
            )
            if st.session_state.FusionRAG:
                if st.session_state.FusionRAG.fusionRAG_query_to_results_map:
                    display_fusionRAG_docs(
                        st.session_state.FusionRAG.fusionRAG_query_to_results_map
                    )
                else:
                    st.warning(
                        "Vuelve cuando hayas preguntado. Todavía no se ha consultado la tienda de vectores."
                    )
    else:
        st.warning(
            "No has creado el Agente Experto. Ve a **configuración** o **evaluación**."
        )
