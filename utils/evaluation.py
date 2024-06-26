import json
from typing import List, Optional

import streamlit as st


def unpack_json(
    uploaded_file: Optional[st.uploaded_file_manager.UploadedFile],
) -> List[dict]:
    """Unpack elements from an uploaded json file.

    Args:
        uploaded_file (Optional[st.uploaded_file_manager.UploadedFile]): The uploaded file object.

    Returns:
        List[dict]: A list of dictionaries, each containing the unpacked elements of a question from the json file.
    """
    unpacked_questions = []  # Initialize an empty list to hold the unpacked questions
    # Ensure there is a file to process
    if uploaded_file is not None:
        # Convert the uploaded file to string
        file_content = uploaded_file.getvalue().decode("utf-8")
        # Parse the JSON content
        json_content = json.loads(file_content)
        # Check if 'preguntas' key exists in json_content
        if "preguntas" in json_content:
            unpacked_questions = build_question_db(json_content["preguntas"])

    return unpacked_questions


def build_question_db(questions_json: List[dict]) -> List[dict]:
    """Build a database of questions from JSON data.

    Args:
        questions_json (List[dict]): JSON with the questions.

    Returns:
        List[dict]: Unpacked questions.
    """
    unpacked_questions = []  # Initialize an empty list to hold the unpacked questions
    for question in questions_json:
        # Construct the unpacked question string
        unpacked_question_str = f'Pregunta: {question["pregunta"]}\n' + "\n".join(
            [f'- OPCIÓN "{o["opcion"]}":  {o["texto"]}' for o in question["opciones"]]
        )
        # Create a dictionary for the current question
        unpackedQ = {
            "id": question["id"],
            "categoria": question[
                "categoria"
            ],  # Added category to the unpacked question
            "unpacked_question": unpacked_question_str,
            "respuesta_correcta": question[
                "respuesta_correcta"
            ],  # Added correct answer to the unpacked question
        }
        # Add the current unpacked question to the list
        unpacked_questions.append(unpackedQ)
    return unpacked_questions
