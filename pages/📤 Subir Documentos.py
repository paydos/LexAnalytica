import streamlit as st

from utils.acknowledge import show_creator_acknowledgement
from utils.pwd import check_password
from utils.session_state_inst import inst_states
from utils.vector_store_uploader import DocumentUploader

inst_states()


st.set_page_config(
    page_title="Documentos",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Documentos del Agente")
if not check_password():
    st.stop()  # Do not continue if check_password is not True.


with st.sidebar:

    st.sidebar.subheader("En caso de que haya un error...")
    if st.button("Reiniciar servicio de subida"):
        st.rerun()

st.markdown("Sube aquí tus documentos y comprueba los que ya están subidos")


uploaded_files = st.file_uploader("Sube aqui los PDFs", accept_multiple_files=True)


if st.button("Subir documentos al Vector Store"):

    with st.spinner("Cargando Vector Store"):
        st.session_state.DocumentUploader = DocumentUploader(
            openai_api_key=st.secrets["OPENAI_API_KEY"],
            openai_embeddings_model="text-embedding-3-large",
            pinecone_api_key=st.secrets["PINECONE_API_KEY"],
            index_name="law-documents",
        )
    if len(uploaded_files) > 0:
        with st.spinner("Subiendo documentos"):
            try:
                st.session_state.DocumentUploader.upload_documents(uploaded_files)
                st.success(f"Se han subido {len(uploaded_files)} documento(s)")
            except Exception as e:
                st.error(f"Ha habido un error subiendo los documento(s):\n{e}")

    else:
        st.warning("No hay ningún documento añadido para subirlo")
show_creator_acknowledgement()
