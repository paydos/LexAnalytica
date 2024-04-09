import streamlit as st
from streamlit_server_state import server_state, server_state_lock

from model import ExpertAgent, FusionRAG
from utils.acknowledge import show_creator_acknowledgement
from utils.pwd import check_password

# Set up Session State
if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None

# Set up Session State
if "ExpertAgentFusionRAG" not in st.session_state:
    st.session_state["ExpertAgentFusionRAG"] = None

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

with server_state_lock["documents"]:
    if "documents" not in server_state:
        server_state.documents = []

st.set_page_config(
    page_title="Ajustes",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="expanded",
)


st.title("Ajustes del Agente Experto")

if not check_password():
    st.stop()  # Do not continue if check_password is not True.


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
    )
    if st.form_submit_button("Añadir descripción del agente"):
        if len(agent_instructions) != 0:
            st.session_state.ExpertAgentInstructions = agent_instructions
            st.success("Descripción del Agente añadida")
        else:
            st.session_state.ExpertAgentInstructions = agent_instructions
            st.warning("El Agente no tiene descripción")

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
        value=1,
        placeholder="Inserta aquí",
    )

with right:
    st.session_state.num_matches_per_branch = st.number_input(
        label="Número de matches por rama",
        min_value=1,
        max_value=5,
        step=1,
        value=1,
        placeholder="Inserta aquí",
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
)
if st.button("Crear FusionRAG"):
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

st.header("Temperatura del Agente")
st.markdown(
    "La temperatura es un parametro en los LLM donde defines cómo de random quieres que sea la respuesta. Cuanto más alto, más probabilidad de que la respuesta no diste mucho de la de un esquizofrénico. Podeis probar a ver que tal funciona. Para que os hagais una idea, el chatGPT tiene 0.7"
)
with st.form("agent_temperature", border=False):
    agent_temperature = st.slider(
        "Temperatura", min_value=0.0, max_value=1.0, step=0.05, value=0.7
    )
    if st.form_submit_button("Configurar temperatura"):
        st.session_state.ExpertAgentTemperature = agent_temperature
        st.success(f"Temperatura configurada a {agent_temperature}")
st.header("Crear Agente Experto")
st.markdown(
    "Una vez ya tengas todas las configuraciones, haz click en 'Generar' para poder empezar a chatear con nuestro Agente"
)
if st.button("Generar"):
    if st.session_state.ExpertAgentTemperature is not None:
        try:
            with st.spinner("Creando Agente"):
                # TODO add updated arguments
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
