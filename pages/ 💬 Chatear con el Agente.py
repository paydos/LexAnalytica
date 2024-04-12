import time
from time import sleep

import streamlit as st

from model import ExpertAgent
from utils.acknowledge import show_creator_acknowledgement
from utils.pwd import check_password
from utils.st_utils import display_fusionRAG_docs

if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None

# Set up Session State
if "FusionRAG" not in st.session_state:
    st.session_state["FusionRAG"] = None

if "ExpertAgentInstructions" not in st.session_state:
    st.session_state["ExpertAgentInstructions"] = ""

if "ExpertAgentTemperature" not in st.session_state:
    st.session_state["ExpertAgentTemperature"] = None

if "DocumentUploader" not in st.session_state:
    st.session_state["DocumentUploader"] = None

if "index_name" not in st.session_state:
    st.session_state["index_name"] = None

if "num_branches_fusionRAG" not in st.session_state:
    st.session_state["num_branches_fusionRAG"] = None

if "num_matches_per_branch" not in st.session_state:
    st.session_state["num_matches_per_branch"] = None

if "context_fusionRAG" not in st.session_state:
    st.session_state["context_fusionRAG"] = None


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

tab1, tab2 = st.tabs(["Chat con el Agente", "Documentos del FusionRAG"])
with tab1:
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

                with st.status("Generando Respuesta", expanded=False) as status:
                    st.session_state.ExpertAgent.chat(user_input, status=status)
                    ai_message = st.session_state.ExpertAgent.ai_message.content

            with st.chat_message("Agente Experto", avatar="🤖"):
                st.markdown(ai_message)
                st.rerun()

    else:
        st.warning(
            "No has creado el Agente. Ve a la configuración y pulsa en **Generar**"
        )
with tab2:
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
