def create_configfile(
    agent_description: str,
    agent_temperature: float,
    fusionRAG_context: str,
    num_matches_per_branch: int,
    num_branches_fusionRAG: int,
) -> str:
    config_content = f"""
    [ExpertAgent]
description = \"\"\"{agent_description}\"\"\"
temperature = {agent_temperature}

[FusionRAG]
context = \"\"\"{fusionRAG_context}\"\"\"
num_matches_per_branch = {num_matches_per_branch}
num_branches = {num_branches_fusionRAG}
    """
    return config_content.strip()
