import binascii
import io
from typing import List
from tqdm import tqdm

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from streamlit.runtime.uploaded_file_manager import UploadedFile


def convert_to_text(pdf_list: List[UploadedFile]) -> List[dict]:
    """
    Converts a list of uploaded PDF files to a list of text chunks with their sources.

    Args:
        pdf_list (List[UploadedFile]): A list of uploaded PDF files.

    Returns:
        List[dict]: A list of dictionaries, each containing 'text' and 'source' keys.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, length_function=len
    )

    docs = []
    for doc in tqdm(pdf_list, desc="Converting PDFs to text"):
        pdf_bytes_io = io.BytesIO(doc.read())
        doc_name = doc.name

        try:
            pdf_doc = PdfReader(pdf_bytes_io)
        except Exception as e:
            raise Exception(f"There was an error reading the pdf: \n{e}")

        text_chunks = []

        for page in tqdm(pdf_doc.pages, desc=f"Processing {doc_name}", leave=False):
            try:
                page_text = page.extract_text()
                if page_text:
                    chunks = splitter.split_text(page_text)
                    for chunk in chunks:
                        text_chunks.append({"text": chunk, "source": doc_name})
            except binascii.Error:
                pass

        docs.extend(text_chunks)
    return docs
