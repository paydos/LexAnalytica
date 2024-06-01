from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Any

import pinecone
import streamlit as st
from langchain.schema import AIMessage, HumanMessage
from langchain_core.documents.base import Document
from langchain_openai import ChatOpenAI
from langchain_pinecone import Pinecone

from utils.vector_store_uploader import DocumentUploader


class FusionRAG(DocumentUploader):
    """
    FusionRAG is a class that inherits from DocumentUploader. It is designed to support RAG and FusionRAG

    The class initializes with API keys for Pinecone and OpenAI, an index name for the
    Pinecone vector store, and the name of the OpenAI embeddings model to use. It then
    loads the Pinecone index and creates an instance of the embeddings model.
    """

    pinecone_api_key: str
    """The API key for Pinecone."""

    openai_api_key: str
    """The API key for OpenAI."""

    index_name: str
    """The name of the Pinecone index to use. Defaults to 'law-documents'."""

    openai_embeddings_model: str
    """The name of the OpenAI embeddings model to use. Defaults to 'text-embedding-3-large'."""

    context: str
    """The context for the FusionRAG. Defaults to ' '."""

    fusionRAG_branches: int
    """The number of FusionRAG branches to create. Defaults to 1."""

    fusionRAG_generated_queries: Optional[List[str]]
    """The list of generated queries for FusionRAG. Defaults to None."""

    results_per_branch: int
    """The number of results per branch. Defaults to 1."""

    vector_store: Optional[Pinecone]
    """The vector store instance."""

    fusionRAGcontext: str
    """The context for FusionRAG queries."""

    fusionRAG_query_to_results_map: Optional[dict]
    """The map of queries to results."""

    def __init__(
        self,
        pinecone_api_key: str,
        openai_api_key: str,
        index_name: str = "law-documents",
        openai_embeddings_model: str = "text-embedding-3-large",
        context: str = " ",
        fusionRAG_branches: int = 1,
        fusionRAG_generated_queries: Optional[List[str]] = None,
        results_per_branch: int = 1,
    ) -> None:
        """Initializes the FusionRAG class with the given parameters.

        Args:
            pinecone_api_key (str): The API key for Pinecone.
            openai_api_key (str): The API key for OpenAI.
            index_name (str, optional): The name of the Pinecone index to use. Defaults to "law-documents".
            openai_embeddings_model (str, optional): The name of the OpenAI embeddings model to use. Defaults to "text-embedding-3-large".
            context (str, optional): The context for FusionRAG. Defaults to " ".
            fusionRAG_branches (int, optional): The number of FusionRAG branches to create. Defaults to 1.
            fusionRAG_generated_queries (List[str], optional): The list of generated queries for FusionRAG. Defaults to None.
            results_per_branch (int, optional): The number of results per branch. Defaults to 1.
        """
        super().__init__(
            pinecone_api_key=pinecone_api_key,
            openai_api_key=openai_api_key,
            index_name=index_name,
            openai_embeddings_model=openai_embeddings_model,
        )
        self.vector_store = None
        self.fusionRAGcontext = context  # Explains "You are an AI Assistant to generate phrases to optimise the search using RAG in a vector store"
        self.fusionRAG_branches = (
            fusionRAG_branches  # "How many fusionRAG branches will be created"
        )
        self.fusionRAG_generated_queries = fusionRAG_generated_queries
        self.fusionRAG_query_to_results_map = None
        self.results_per_branch = results_per_branch

        self._create_embeddings_model()
        self._vectorstore_instances()

    def _vectorstore_instances(self) -> None:
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

    def _consult_vectorstore_threaded(self, query: str) -> List[Document]:
        return self.consult_vectorstore(query, self.results_per_branch)

    def fusion_rag(
        self, chat_completions: ChatOpenAI, human_msg: str, status: Any
    ) -> List[Document]:
        """Generates FusionRAG queries and consults the vector store.

        Args:
            chat_completions (ChatOpenAI): The ChatOpenAI instance for generating queries.
            human_msg (str): The human message to generate queries for.
            status (Any): The status object for updating the UI.

        Returns:
            List[Document]: The list of documents retrieved from the vector store.
        """

        # Template to generate vectorstore queries
        vectorstore_fusionRAG_query = HumanMessage(
            content=f"""
        AI Assistant purpose: {self.fusionRAGcontext}
                
        Number of phrases for RAG querying: {self.fusionRAG_branches}. Return each query in one line to split them.
        
        User question: {human_msg}
        """
        )

        response_content = chat_completions.invoke(
            vectorstore_fusionRAG_query.content
        ).content

        # Generated queries
        self.fusionRAG_generated_queries = response_content.strip().split("\n")

        if hasattr(status, "update"):
            with status:
                containerBranch = st.container()
                with containerBranch:
                    containerBranch.empty()  # Empty the previous content
                    for query in self.fusionRAG_generated_queries:
                        st.write(query)

        print(f"{len(self.fusionRAG_generated_queries)} KNOWLEDGE BRANCHES GENERATED")
        for branch in self.fusionRAG_generated_queries:
            print(f"KNOWLEDGE BRANCH: {branch}")

        vectorstore_results = []
        query_to_results_map = {}

        with ThreadPoolExecutor() as executor:
            futures = {
                query: executor.submit(self._consult_vectorstore_threaded, query)
                for query in self.fusionRAG_generated_queries
            }
            for query, future in futures.items():
                result = future.result()
                vectorstore_results.extend(result)
                query_to_results_map[query] = result

        self.fusionRAG_query_to_results_map = query_to_results_map

        return vectorstore_results

    def consult_vectorstore(self, query: str, how_many: int = 3) -> List[Document]:
        """
        Consults the VectorStore for a given string query.

        Args:
            query (str): The query string to search for.
            how_many (int, optional): The number of results to return. Defaults to 3.

        Returns:
            List[Document]: The list of documents retrieved from the vector store.
        """
        results = self.vector_store.similarity_search(query, k=how_many)
        return results
