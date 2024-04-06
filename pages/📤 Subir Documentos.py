import streamlit as st

from model.LLM import ExpertAgent

st.set_page_config(
    page_title="Documentos",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Documentos del Agente")
