import streamlit as st


def waiting_messages(message, placeholder, bot_chatholder):
    with placeholder.container():
        with bot_chatholder:
            st.markdown(f"{message}")
