import streamlit as st
import toml

if "ExpertAgent" not in st.session_state:
    st.session_state["ExpertAgent"] = None


# Set up Session State
def load_config(config_file):
    config = toml.loads(config_file)
    st.session_state["ExpertAgentInstructions"] = config["ExpertAgent"]["description"]
    st.session_state["ExpertAgentTemperature"] = config["ExpertAgent"]["temperature"]
    st.session_state["num_branches_fusionRAG"] = config["FusionRAG"]["num_branches"]
    st.session_state["num_matches_per_branch"] = config["FusionRAG"][
        "num_matches_per_branch"
    ]
    st.session_state["context_fusionRAG"] = config["FusionRAG"]["context"]
