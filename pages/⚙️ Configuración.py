import streamlit as st
from streamlit_server_state import server_state, server_state_lock

from model.LLM import ExpertAgent
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
    agent_instructions = st.text_input(
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
                st.session_state.ExpertAgent = ExpertAgent(
                    api_key=st.secrets["OPENAI_API_KEY"],
                    model_name=st.secrets["MODEL_NAME"],
                    agent_description=st.session_state.ExpertAgentInstructions,
                    temperature=st.session_state.ExpertAgentTemperature,
                )
            st.success("El Agente se ha creado correctamente")
        except Exception as e:
            st.error(f"No se ha podido crear el Agente: \n{e}", icon="💀")
    else:
        st.error(
            f"La temperatura del agente es {st.session_state.ExpertAgentTemperature}. No te olvides de hacer click en **Configurar temperatura**"
        )

show_creator_acknowledgement()
