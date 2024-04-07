import streamlit as st
from streamlit_server_state import server_state, server_state_lock

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

if st.button("Resetear índice del Vector Store"):
    with server_state_lock["index_name"]:
        server_state.index_name = index_name  # Reset to default index name
        st.success(f"Índice del Vector Store reseteado a '{index_name}'")

if st.button("Resetear documentos subidos"):
    with server_state_lock["documents"]:
        server_state.documents = []
        st.success("Documentos del Vector Store reseteados.")
