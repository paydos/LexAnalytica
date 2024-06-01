from typing import List

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def convert2bytes(files: List[UploadedFile]) -> List[bytes]:
    """Converts a list of UploadedFile objects to a list of bytes.

    Args:
        files (List[UploadedFile]): A list of UploadedFile objects to be converted.

    Returns:
        List[bytes]: A list of byte contents of the uploaded files.
    """
    to_return = []
    for file in files:
        to_return.append(file.read())
    return to_return
