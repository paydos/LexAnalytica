import time

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from model.LLM import ExpertAgent
from model.RAG import FusionRAG
from utils.evaluation import unpack_json
from utils.pwd import check_password
from utils.session_state_inst import inst_states
from utils.st_utils import display_results, load_config

inst_states()


st.set_page_config(
    page_title="Evaluación 📊",
    page_icon="data/branded_icon.png",
    initial_sidebar_state="collapsed",
)


st.title("Evaluación 📊")
if not check_password():

    st.stop()  # Do not continue if check_password is not True.

if not st.session_state.ExpertAgent_finished:
    if (
        "examination_json" not in st.session_state
        or st.session_state["examination_json"] is None
    ):
        st.header("Paso 1: Cargar el JSON con las preguntas")
        st.markdown(
            "Para poder evaluar el Agente Experto, arrastra el json en la caja del medio de la pantalla"
        )
        examination_files = st.file_uploader(
            "Sube aquí el json",
            accept_multiple_files=False,
            label_visibility="collapsed",
        )

        if examination_files is not None:

            st.session_state["examination_json"] = examination_files
            st.rerun()
    else:
        st.success("Archivo cargado con éxito.")

    st.session_state.unpackedQuestions = unpack_json(st.session_state.examination_json)

    if st.session_state.unpackedQuestions:
        st.header("Archivos cargados:")
        st.markdown(
            "Haz click en las preguntas para comprobar que se han cargado correctamente"
        )
        for question in st.session_state.unpackedQuestions:
            with st.expander(
                f"📝 Pregunta ID: {question['id']} - Categoría: {question['categoria']}"
            ):
                st.subheader(f"🔍 {question['unpacked_question']}")
                st.markdown(
                    f"**✅ Respuesta Correcta:** {question['respuesta_correcta']}"
                )
            question["unpacked_question"] = (
                f"Categoría: {question['categoria']} \n{question['unpacked_question']}"
            )

    else:
        st.write("❌ No se ha subido ningún archivo JSON o el archivo está vacío.")
    if st.session_state.unpackedQuestions:
        st.header("Paso 2: Cargar los prompts + configuración")
        st.markdown(
            "El archivo que entregamos (ENTREGA.toml) tiene los prompts y parámetros óptimos. Pulsa en configuración, y en el lado izquiero verás un botón de **cargar configuración**. Puede tardar hasta 2 minutos en instanciar el Agente Experto."
        )
        uploaded_config = st.file_uploader(
            label="Sube aquí tu configuración",
            accept_multiple_files=False,
            type="toml",
            label_visibility="collapsed",
        )
        if uploaded_config:
            config_string = uploaded_config.getvalue().decode("utf-8")
            load_config(config_string)
            st.session_state["config_loaded"] = True

        if st.button("Generar un asistente LexAnalytica"):
            try:
                with st.spinner("Creando Agente"):
                    st.session_state.FusionRAG = FusionRAG(
                        openai_api_key=st.secrets["OPENAI_API_KEY"],
                        pinecone_api_key=st.secrets["PINECONE_API_KEY"],
                        index_name="law-documents",
                        context=st.session_state.context_fusionRAG,
                        fusionRAG_branches=st.session_state.num_branches_fusionRAG,
                        results_per_branch=st.session_state.num_matches_per_branch,
                    )
                st.success("El RAG se ha creado correctamente")
            except Exception as e:
                st.error(f"No se ha podido crear el RAG: \n{e}", icon="💀")

            try:
                with st.spinner("Creando Agente"):
                    st.session_state.ExpertAgent = ExpertAgent(
                        api_key=st.secrets["OPENAI_API_KEY"],
                        model_name=st.secrets["MODEL_NAME"],
                        agent_description=st.session_state.ExpertAgentInstructions,
                        temperature=st.session_state.ExpertAgentTemperature,
                        fusion_rag=st.session_state.FusionRAG,
                    )
                st.session_state.examMode = True
                st.success("El Agente se ha creado correctamente")

                st.markdown(
                    f"Ya puedes probar al Agente Experto con la batería de preguntas. Has cargado un total de {len(st.session_state.unpackedQuestions)} preguntas"
                )

                # switch_page("Chatear con el Agente")
                waiting = st.progress(100)
                for i in range(100):
                    time.sleep(0.02)
                    waiting.progress(i, "Cambiando de página")
                switch_page("Chatear con el Agente")

            except Exception as e:
                st.error(f"Error al crear el Agente: {e}", icon="🚨")

else:
    st.header("Resultados de evaluación")
    st.markdown(
        f"""A continuación se muestran las respuestas y los resultados de la evaluación. Para un total de **{len(st.session_state.unpackedQuestions)} preguntas**, estas han sido las respuestas:"""
    )
    # add here display of answers + download json with responses
    display_results(
        ExpertAgentInstance=st.session_state.ExpertAgent,
    )
