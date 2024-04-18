import streamlit as st


def inst_states():
    # Set up Session State
    if "ExpertAgent" not in st.session_state:
        st.session_state["ExpertAgent"] = None

    # Set up Session State
    if "FusionRAG" not in st.session_state:
        st.session_state["FusionRAG"] = None

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

    if "examMode" not in st.session_state:
        st.session_state["examMode"] = False

    if "unpackedQuestions" not in st.session_state:
        st.session_state["unpackedQuestions"] = None

    if "examination_json" not in st.session_state:
        st.session_state["examination_json"] = None

    if "ExpertAgent_finished" not in st.session_state:
        st.session_state["ExpertAgent_finished"] = False

    if "raw_json" not in st.session_state:
        st.session_state["raw_json"] = None
