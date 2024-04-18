import re

import streamlit as st
import toml

from model import ExpertAgent

if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None


# Set up Session State
def load_config(config_file):
    config = toml.loads(config_file)
    st.session_state["ExpertAgentInstructions"] = config["ExpertAgent"]["description"]
    st.session_state["ExpertAgentTemperature"] = float(
        config["ExpertAgent"]["temperature"]
    )
    st.session_state["num_branches_fusionRAG"] = config["FusionRAG"]["num_branches"]
    st.session_state["num_matches_per_branch"] = config["FusionRAG"][
        "num_matches_per_branch"
    ]
    st.session_state["context_fusionRAG"] = config["FusionRAG"]["context"]


def display_fusionRAG_docs(fusionRAG_query_to_results_map):
    for query, chunks in fusionRAG_query_to_results_map.items():
        st.subheader(f"Consulta: {query}")
        for i, chunk in enumerate(chunks):
            with st.expander(
                label=f"Fuente {i+1} de {len(chunks)}: {chunk.metadata['source']}"
            ):
                st.markdown(chunk.page_content)


def display_results(ExpertAgentInstance: ExpertAgent):
    """
    Unpack from ExpertAgent's object

    When unpacking the questions, [0,1] are not unpacked as they correspond to context + useless response
    """

    import json

    if hasattr(ExpertAgentInstance, "chat_history"):
        chat_history_json = []
        for i in range(2, len(ExpertAgentInstance.chat_history) - 1, 2):
            question = ExpertAgentInstance.chat_history[i]
            answer = ExpertAgentInstance.chat_history[i + 1]
            try:
                chat_history_json.append(
                    {
                        "pregunta": question.content,
                        "respuesta": (
                            re.search(r'"([A-Z])"|([A-Z])\)', answer.content).group(1)
                            if re.search(r'"([A-Z])"', answer.content)
                            else (
                                re.search(r"([A-Z])\)", answer.content).group(1)
                                if re.search(r"([A-Z])\)", answer.content)
                                else "Ha habido un error parseando. La respuesta estará en la justificación"
                            )
                        ),
                        "justificacion": answer.content,
                    }
                )
            except:
                chat_history_json.append(
                    {
                        "pregunta": question.content,
                        "respuesta": "Se ha parseado mal, mira en la justificación",
                        "justificacion": answer.content,
                    }
                )

    for i, exam_question in enumerate(
        json.loads(st.session_state["examination_json"].getvalue().decode("utf-8"))[
            "preguntas"
        ]
    ):
        question = ExpertAgentInstance.chat_history[i * 2 + 2]
        answer = ExpertAgentInstance.chat_history[i * 2 + 3]
        correct_answer = exam_question["respuesta_correcta"]
        try:
            extracted_answer = (
                re.search(r'"([A-Z])"|([A-Z])\)', answer.content).group(1)
                if re.search(r'"([A-Z])"', answer.content)
                or re.search(r"([A-Z])\)", answer.content)
                else "Error en la extracción de la respuesta"
            )
        except:
            extracted_answer = "Z"
        is_correct = "✅" if extracted_answer == correct_answer else "❌"
        print(f"QUESTION {i}: {is_correct}")

        with st.expander(label=f"Pregunta {i + 1} {is_correct}"):
            st.subheader("Pregunta")
            st.markdown(f"{question.content}")
            st.subheader("Respuesta")
            st.markdown(f"{answer.content}")
            st.subheader("Resultado")
            st.markdown(f"Respuesta proporcionada: **{extracted_answer}**")
            st.markdown(f"Respuesta correcta: **{correct_answer}**")
    if st.download_button(
        label="Descargar respuestas",
        data=json.dumps(chat_history_json, ensure_ascii=False, indent=4).encode(
            "utf-8"
        ),
        file_name="RESPUESTAS.json",
        mime="application/json",
    ):
        st.success("Historial de chat descargado con éxito.")


import re

import streamlit as st
import toml

from model import ExpertAgent

if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None


# Set up Session State
def load_config(config_file):
    config = toml.loads(config_file)
    st.session_state["ExpertAgentInstructions"] = config["ExpertAgent"]["description"]
    st.session_state["ExpertAgentTemperature"] = float(
        config["ExpertAgent"]["temperature"]
    )
    st.session_state["num_branches_fusionRAG"] = config["FusionRAG"]["num_branches"]
    st.session_state["num_matches_per_branch"] = config["FusionRAG"][
        "num_matches_per_branch"
    ]
    st.session_state["context_fusionRAG"] = config["FusionRAG"]["context"]


def display_fusionRAG_docs(fusionRAG_query_to_results_map):
    for query, chunks in fusionRAG_query_to_results_map.items():
        st.subheader(f"Consulta: {query}")
        for i, chunk in enumerate(chunks):
            with st.expander(
                label=f"Fuente {i+1} de {len(chunks)}: {chunk.metadata['source']}"
            ):
                st.markdown(chunk.page_content)
