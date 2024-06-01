def create_configfile(
    agent_description: str,
    agent_temperature: float,
    fusionRAG_context: str,
    num_matches_per_branch: int,
    num_branches_fusionRAG: int,
) -> str:
    """Creates a configuration file content.

    Args:
        agent_description (str): Description of the agent.
        agent_temperature (float): Temperature setting for the agent.
        fusionRAG_context (str): Context for FusionRAG.
        num_matches_per_branch (int): Number of matches per branch.
        num_branches_fusionRAG (int): Number of branches for FusionRAG.

    Returns:
        str: The content of the configuration file.
    """
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
