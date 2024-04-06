import streamlit as st
from streamlit_server_state import server_state, server_state_lock

from utils.pdf2txt import convert_to_text
from utils.vector_store_uploader import DocumentUploader

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
    st.session_state["index_name"] = "law-documents"

with server_state_lock["documents"]:
    if "documents" not in server_state:
        server_state.documents = []


st.set_page_config(
    page_title="Documentos",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Documentos del Agente")

st.markdown("Sube aquí tus documentos y comprueba los que ya están subidos")

st.session_state.DocumentUploader = DocumentUploader(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    openai_embeddings_model="text-embedding-3-large",
    pinecone_api_key=st.secrets["PINECONE_API_KEY"],
    index_name=st.session_state.index_name,
)

uploaded_files = st.file_uploader("Sube aqui los PDFs", accept_multiple_files=True)


if st.button("Subir documentos al Vector Store"):
    if len(uploaded_files) > 0:
        with server_state_lock["documents"]:
            # Filter out files that are already in server_state.documents
            new_files = []
            for file in uploaded_files:
                if file.name not in server_state["documents"]:
                    new_files.append(file)
                    server_state["documents"].append(file.name)
                else:
                    st.warning(f"El archivo '{file.name}' ya está subido.")
        if new_files:  # Check if there are any new files to upload after filtering
            with st.spinner("Subiendo documentos"):
                st.session_state.DocumentUploader.upload_documents(uploaded_files)
        else:
            st.warning(
                "Todos los documentos seleccionados ya han sido subidos anteriormente."
            )
    else:
        st.warning("No hay ningún documento añadido para subirlo")

# Display the names of uploaded documents from server_state.documents list using markdown and bullet points
if server_state.documents:
    st.markdown("### Documentos subidos:")
    col1, col2 = st.columns(2)
    half = len(server_state.documents) // 2
    with col1:
        for document in server_state.documents[:half]:
            st.markdown(f"📄 `{document}`")
    with col2:
        for document in server_state.documents[half:]:
            st.markdown(f"📄 `{document}`")
else:
    st.write("No hay documentos subidos aún.")
