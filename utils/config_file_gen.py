def create_configfile(
    agent_description: str,
    agent_temperature: float,
    fusionRAG_context: str,
    num_matches_per_branch: int,
    num_branches_fusionRAG: int,
) -> str:
    """_summary_

    Args:
        agent_description (str): _description_
        agent_temperature (float): _description_
        fusionRAG_context (str): _description_
        num_matches_per_branch (int): _description_
        num_branches_fusionRAG (int): _description_

    Returns:
        str: _description_
    """ """"""
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
