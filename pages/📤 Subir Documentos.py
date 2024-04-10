import streamlit as st
from streamlit_server_state import server_state, server_state_lock

from utils.acknowledge import show_creator_acknowledgement
from utils.pdf2txt import convert_to_text
from utils.pwd import check_password
from utils.vector_store_uploader import DocumentUploader

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
    page_title="Documentos",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Documentos del Agente")
if not check_password():
    st.stop()  # Do not continue if check_password is not True.


with st.sidebar:
    if server_state.documents:
        st.sidebar.markdown("### Documentos subidos:")
        for document in server_state.documents:
            st.sidebar.markdown(f"📄 `{document}`")

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
                try:
                    st.session_state.DocumentUploader.upload_documents(uploaded_files)
                except Exception as e:
                    st.error(f"Ha habido un error subiendo los documento(s):\n{e}")
        else:
            st.warning(
                "Todos los documentos seleccionados ya han sido subidos anteriormente."
            )
    else:
        st.warning("No hay ningún documento añadido para subirlo")

# Display the names of uploaded documents from server_state.documents list using markdown and bullet points
