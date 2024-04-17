import streamlit as st
import toml

from model import ExpertAgent, FusionRAG
from utils.acknowledge import show_creator_acknowledgement
from utils.config_file_gen import create_configfile
from utils.pwd import check_password
from utils.session_state_inst import inst_states
from utils.st_utils import load_config

inst_states()

st.set_page_config(
    page_title="Ajustes 🔧",
    page_icon="data/branded_icon.png",
    layout="centered",
    initial_sidebar_state="expanded",
)

disabled = st.session_state.examMode  # Variable to disable all inputs

st.title("Ajustes del Agente Experto")

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

with st.sidebar:
    st.sidebar.header("Exportar configuración")
    st.sidebar.markdown(
        "Pulsa el botón para descargar la configuración actual. Esto incluye la **descripción** del Agente y el FusionRAG, el **número de ramas** y **resultados por rama**, así como también la temperatura."
    )
    if None not in [
        st.session_state.ExpertAgentInstructions,
        st.session_state.ExpertAgentTemperature,
        st.session_state.context_fusionRAG,
        st.session_state.num_matches_per_branch,
        st.session_state.num_branches_fusionRAG,
    ]:
        if st.download_button(
            label="Exportar configuración",
            data=create_configfile(
                agent_description=st.session_state.ExpertAgentInstructions,
                agent_temperature=st.session_state.ExpertAgentTemperature,
                fusionRAG_context=st.session_state.context_fusionRAG,
                num_matches_per_branch=st.session_state.num_matches_per_branch,
                num_branches_fusionRAG=st.session_state.num_branches_fusionRAG,
            ),
            file_name="ExpertAgentCONFIG.toml",
            disabled=disabled,
        ):
            st.success("Archivo de configuración exportado")
    else:
        st.warning("No se puede exportar la configuración porque falta información.")
    st.sidebar.header("Cargar configuración")
    st.sidebar.markdown(
        "Arrastra o pulsa aquí para cargar la configuración del Agente. Puedes modificarla después y volver a descargarla."
    )
    uploaded_config = st.file_uploader(
        label="Sube aquí tu configuración",
        accept_multiple_files=False,
        type="toml",
        label_visibility="collapsed",
        disabled=disabled,
    )
    if uploaded_config:
        config_string = uploaded_config.getvalue().decode("utf-8")
        load_config(config_string)
        uploaded_config.close()


st.markdown(
    "Aquí están los ajustes del Agente Experto. Ve haciendo scrolldown para explorar todos los ajustes y cambiarlos como veas."
)

with st.form("agent_instructions", border=False):
    st.markdown(
        "Introduce aquí la descripción de nuestro Agente Experto. Recuerda que aquí debes describir quien es, que debe hacer, etc"
    )
    agent_instructions = st.text_area(
        label="Descripción del asistente",
        placeholder="Inserta aqui la descripción del agente",
        value=st.session_state.ExpertAgentInstructions,
        disabled=disabled,
    )
    if st.form_submit_button("Añadir descripción del agente", disabled=disabled):
        if len(agent_instructions) != 0:
            st.session_state.ExpertAgentInstructions = agent_instructions
            st.success("Descripción del Agente añadida")
        else:
            st.session_state.ExpertAgentInstructions = agent_instructions
            st.warning("El Agente no tiene descripción")

st.header("Temperatura del Agente")
st.markdown(
    "La temperatura es un parametro en los LLM donde defines cómo de random quieres que sea la respuesta. Cuanto más alto, más probabilidad de que la respuesta sea muy de Vincent van Gogh. Podeis probar a ver que tal funciona. Para que os hagais una idea, el chatGPT tiene 0.7"
)
with st.form("agent_temperature", border=False):
    agent_temperature = st.slider(
        "Temperatura",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        value=st.session_state.ExpertAgentTemperature,
        disabled=disabled,
    )
    if st.form_submit_button("Configurar temperatura", disabled=disabled):
        st.session_state.ExpertAgentTemperature = agent_temperature
        st.success(f"Temperatura configurada a {agent_temperature}")
st.header("Configuración del FusionRAG")
st.markdown("Configura cómo se va a comportar el FusionRAG")

st.subheader("Número de ramas del FusionRAG")
st.markdown(
    """El **número de ramas** del FusionRAG es el número de consultas que queremos hacer a la VectorStore (Donde tenemos los documentos).
            Digamos que es, el número de veces que "podemos preguntar" a una persona que sabe mucho del tema.
            El **número de matches por rama** es cuántos resultados queremos por cada rama.
            
            """
)

left, center, right = st.columns(3)

with left:
    st.session_state.num_branches_fusionRAG = st.number_input(
        label="Número de ramas",
        min_value=1,
        max_value=5,
        step=1,
        value=st.session_state.num_branches_fusionRAG,
        placeholder="Inserta aquí",
        disabled=disabled,
    )

with right:
    st.session_state.num_matches_per_branch = st.number_input(
        label="Número de matches por rama",
        min_value=1,
        max_value=5,
        step=1,
        value=st.session_state.num_matches_per_branch,
        placeholder="Inserta aquí",
        disabled=disabled,
    )

st.subheader("Contexto del FusionRAG")
st.markdown(
    """
            El **contexto** te permite decirle al fusionRAG que hacer con el input del usuario y cómo procesarlo para transformarlo en búsquedas. Pongo un ejemplo:
            
            _Eres un AI Assistant que coge el input del usuario y transforma la pregunta del usuario en frases para mejorar el resultado del RAG en búsquedas de un vector store. Cuando transformes el input, genera las frases teniendo en cuenta X e Y. Omite palabras A, B y C..._
            """
)

st.session_state.context_fusionRAG = st.text_area(
    "Inserta aquí el contexto para el FusionRAG.",
    placeholder="Escribe aquí el contexto para el FusionRAG",
    value=st.session_state.context_fusionRAG,
    disabled=disabled,
)
if st.button("Crear FusionRAG", disabled=disabled):
    if (
        st.session_state.num_branches_fusionRAG is None
        or st.session_state.num_matches_per_branch is None
        or st.session_state.context_fusionRAG == ""
    ):
        if st.session_state.num_branches_fusionRAG is None:
            st.warning("No puedes crear el FusionRAG sin indicar el número de ramas")
        if st.session_state.num_matches_per_branch is None:
            st.warning(
                "No puedes crear el FusionRAG sin indicar el número de matches por rama"
            )
        if st.session_state.context_fusionRAG == "":
            st.warning("No puedes crear el FusionRAG sin indicar el contexto")

    else:
        try:
            with st.spinner("Creando Agente"):
                # TODO add updated arguments
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

st.header("Crear Agente Experto")
st.markdown(
    "Una vez ya tengas todas las configuraciones, haz click en 'Generar' para poder empezar a chatear con nuestro Agente"
)
if st.button("Generar", disabled=disabled):
    if st.session_state.ExpertAgentTemperature is not None:
        try:
            with st.spinner("Creando Agente"):
                st.session_state.ExpertAgent = ExpertAgent(
                    api_key=st.secrets["OPENAI_API_KEY"],
                    model_name=st.secrets["MODEL_NAME"],
                    agent_description=st.session_state.ExpertAgentInstructions,
                    temperature=st.session_state.ExpertAgentTemperature,
                    fusion_rag=st.session_state.FusionRAG,
                )
            st.success("El Agente se ha creado correctamente")
        except Exception as e:
            st.error(f"Error al crear el Agente: {e}", icon="🚨")
    else:
        st.error(
            f"La temperatura del agente es {st.session_state.ExpertAgentTemperature}. No te olvides de hacer click en **Configurar temperatura**"
        )


show_creator_acknowledgement()
