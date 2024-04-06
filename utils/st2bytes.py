from typing import List

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def convert2bytes(files: List[UploadedFile]):
    to_return = []
    for file in files:
        to_return.append(file.read())
    return to_return
