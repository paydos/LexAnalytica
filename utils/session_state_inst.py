import streamlit as st


def inst_states():
    # Define default session state values
    default_values = {
        "ExpertAgent": None,
        "FusionRAG": None,
        "ExpertAgentInstructions": "",
        "ExpertAgentTemperature": None,
        "DocumentUploader": None,
        "index_name": None,
        "num_branches_fusionRAG": None,
        "num_matches_per_branch": None,
        "context_fusionRAG": None,
        "examMode": False,
        "unpackedQuestions": None,
        "examination_json": None,
        "ExpertAgent_finished": False,
        "raw_json": None,
    }

    # Set up Session State with default values if not already present
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value
