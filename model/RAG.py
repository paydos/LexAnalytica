from typing import List

import pinecone
import streamlit as st
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_core.documents.base import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone

from utils.vector_store_uploader import DocumentUploader


class FusionRAG(DocumentUploader):
    """
    FusionRAG is a class that inherits from DocumentUploader. It is designed to support RAG and FusionRAG

    The class initializes with API keys for Pinecone and OpenAI, an index name for the
    Pinecone vector store, and the name of the OpenAI embeddings model to use. It then
    loads the Pinecone index and creates an instance of the embeddings model.

    Attributes:
        - pinecone_api_key (str): The API key for Pinecone.
        - openai_api_key (str): The API key for OpenAI.
        - index_name (str): The name of the Pinecone index to use. Defaults to "law-documents".
        - openai_embeddings_model (str): The name of the OpenAI embeddings model to use.
                                       Defaults to "text-embedding-3-large".
    """

    def __init__(
        self,
        pinecone_api_key: str,
        openai_api_key: str,
        index_name: str = "law-documents",
        openai_embeddings_model: str = "text-embedding-3-large",
        context: str = " ",
        fusionRAG_branches: int = 1,
        fusionRAG_queries: List[str] = None,
    ) -> None:
        super().__init__(
            pinecone_api_key=pinecone_api_key,
            openai_api_key=openai_api_key,
            index_name=index_name,
            openai_embeddings_model=openai_embeddings_model,
        )
        self.vector_store = None
        self.context = context
        self.fusionRAG_branches = fusionRAG_branches
        self.fusionRAG_queries = fusionRAG_queries

        self._create_embeddings_model()
        self._vectorstore_instances()

    def _vectorstore_instances(self):
        """
        Loads Pinecone instances (Pinecone from langchain.vectorstores)
        - Creates Pinecone instance
        - Creates Pinecone.Index instance
        - Creates vectorstore instance
        """
        self.pc = pinecone.Pinecone(api_key=self.pinecone_api_key)
        self.Index = self.pc.Index(self.index_name)
        self.Pinecone = Pinecone
        self.vector_store = self.Pinecone(
            self.Index, self.embeddings_model, self.text_field
        )

    def generate_queries(self, input_query):

        pass

    def consult_vectorstore(self, query: str, how_many: int = 3) -> List[Document]:
        """
        Consults the VectorStore for a given string query.
        - Returns a list
        """
        results = self.vector_store.similarity_search(query, k=how_many)

        return results
