from time import sleep

import streamlit as st

from constants import OPENAI_API_KEY, MODEL_NAME
from model import ExpertAgent

# Set up Session State
if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None

if "ExpertAgentInstructions" not in st.session_state:
    st.session_state["ExpertAgentInstructions"] = ""

if "ExpertAgentTemperature" not in st.session_state:
    st.session_state["ExpertAgentTemperature"] = None


def main():
    st.sidebar.title("Ajustes del Agente Experto")

    with st.sidebar:
        st.markdown(
            "Aquí están los ajustes del Agente Experto. Ve haciendo scrolldown para explorar todos los ajustes y cambiarlos como veas."
        )
        st.sidebar.header("Descripción del Agente")

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

        st.header("Resetear memoria del agente")
        st.markdown(
            "Si quieres empezar de cero, con los ajustes y descripciones que ya has puesto, pero sin que el Agente se acuerde nada, pulsa el botón a continuación"
        )
        # Reset Memory
        if st.button("Borrar memoria del agente"):
            if st.session_state.ExpertAgent:
                try:
                    st.session_state.ExpertAgent.chat_history = []
                    reset_banner = st.success("Memoria borrada")
                    sleep(0.5)
                    reset_banner.empty()

                except Exception as e:
                    st.error(f"La memoria no ha sido reseteada:\n {e}", icon="🧠")
            else:
                st.error(
                    "La memoria no se puede resetear porque no has creado un Agente"
                )

        st.header("Crear Agente Experto")
        st.markdown(
            "Una vez ya tengas todas las configuraciones, haz click en 'Generar' para poder empezar a chatear con nuestro Agente"
        )

        if st.button("Generar"):
            try:
                with st.spinner("Creando Agente"):
                    st.session_state.ExpertAgent = ExpertAgent(
                        api_key=OPENAI_API_KEY,
                        model_name=MODEL_NAME,
                        agent_description=st.session_state.ExpertAgentInstructions,
                        temperature=st.session_state.ExpertAgentTemperature,
                    )
                st.success("El Agente se ha creado correctamente")
            except Exception as e:
                st.error(f"No se ha podido crear el Agente: \n{e}", icon="💀")

    # Prints the whole convo
    if st.session_state.ExpertAgent:
        if st.session_state.ExpertAgent.chat_history:
            for message in st.session_state.ExpertAgent.chat_history[2:]:
                if message.type == "human":
                    with st.chat_message(message.content, avatar="👨"):
                        st.markdown(message.content)
                else:
                    with st.chat_message(message.content, avatar="🤖"):
                        st.markdown(message.content)
    user_input = st.chat_input("Escribe aquí tu consulta al agente experto")

    if user_input:
        with st.chat_message("user", avatar="👨"):
            st.markdown(user_input)

        # Show a typing indicator while the agent is processing the input
        with st.chat_message("Agente Experto", avatar="🤖"):

            with st.spinner("Generando Respuesta"):
                st.session_state.ExpertAgent.chat(user_input)
                ai_message = st.session_state.ExpertAgent.ai_message.content

        with st.chat_message("Agente Experto", avatar="🤖"):
            st.markdown(ai_message)

        st.rerun()


if __name__ == "__main__":
    main()
