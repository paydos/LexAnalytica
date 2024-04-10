import streamlit as st

from utils.acknowledge import show_creator_acknowledgement
from utils.pwd import check_password

st.title("Ajustes de Desarrollador")
if not check_password():
    st.stop()  # Do not continue if check_password is not True.


st.warning(
    "Esta página no está destinada para uso general. Es solo para configuración interna."
)

# Set the index name for the vector store using session state
index_name = st.text_input(
    "Introduce el nombre del índice para el Vector Store:", value="law-documents"
)

# Disclaimer message
st.info(
    "⚠️ Cambiar el nombre del índice afectará a dónde se suben y se buscan los documentos."
)

# Button to reload the whole Streamlit app
if st.button("Recargar aplicación"):
    st.rerun()


show_creator_acknowledgement()
