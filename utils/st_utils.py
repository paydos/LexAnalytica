import streamlit as st
import toml

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
