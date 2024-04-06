import streamlit as st
from streamlit_server_state import server_state, server_state_lock

# Set up Session State
if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None

if "ExpertAgentInstructions" not in st.session_state:
    st.session_state["ExpertAgentInstructions"] = ""

if "ExpertAgentTemperature" not in st.session_state:
    st.session_state["ExpertAgentTemperature"] = None

if "DocumentUploader" not in st.session_state:
    st.session_state["DocumentUploader"] = None

with server_state_lock["documents"]:
    if "documents" not in server_state:
        server_state.documents = []


st.set_page_config(
    page_title="Menú principal",
    page_icon="👋",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.write("# Bienvenido al Agente Experto 👋")
st.markdown("Antes de empezar leete esto :)")
st.title("Guía de Uso del Agente Experto")
st.markdown(
    """
    
    En caso de que haya quedado alguna duda tras la reunión, aquí tienes una guía breve sobre cómo utilizar este Agente:
    
    - Próximamente incluiremos un contador para llevar un registro de los gastos acumulados tanto por nuestra parte como por la vuestra.
    - Es posible que surjan errores durante el uso del Agente. Si esto ocurre, por favor, toma una captura de pantalla del error y envíanosla por WhatsApp.
    """
)
st.header("Cómo usar la aplicación")
st.subheader("Secciones")
st.markdown(
    """
- La primera sección es la actual, donde se encuentra la documentación.
- La segunda sección incluye todos los ajustes disponibles para su configuración. He incluido explicaciones aquí para que se entienda mejor.
- Finalmente, la tercera sección es el chat, donde pueden realizar pruebas interactuando con el Agente.

Para poder cambiar entre secciones, arriba a la izquierda tienes una flechita para hacer click.
"""
)

st.subheader("Configuración y tuning del Agente")
st.markdown(
    """
Le he metido bastantes cosillas para que podamos tune it cuanto queramos. Iré añadiendo más cosas si veo que es necesario.
Los ajustes que podeis tocar son:
- **Descripción:** Aquí se añade la "personalidad" ejem ejem, de nuestro Agente. Cuando hayáis terminado de escribirla le dais a **Añadir descripción del agente** 
- **Temperatura:** El verano está cerca, pero no es sobre esto 😂. Este parámetro configura lo "loco" que está nuestro Agente. Le pones un 0 y has creado el Agente más soso del mundo. Le pones un 1 y está de manicomio. Como referencia, ChatGPT usa 0.7.
            
            """
)