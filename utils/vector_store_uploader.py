import time
from typing import List, Optional

from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, PodSpec
from tqdm import tqdm

from utils.pdf2txt import convert_to_text


class DocumentUploader:
    pinecone_api_key: str
    """The API key for Pinecone."""

    openai_api_key: str
    """The API key for OpenAI."""

    openai_embeddings_model: str
    """The name of the OpenAI embeddings model to use."""

    index_name: str
    """The name of the Pinecone index to use."""

    text_field: str
    """The field name for the text in the documents."""

    Index: Optional[Pinecone.Index]
    """The Pinecone index instance."""

    Pinecone: Optional[Pinecone]
    """The Pinecone instance."""

    embeddings_model: Optional[OpenAIEmbeddings]
    """The OpenAI embeddings model instance."""

    chunked_text: Optional[List[dict]]
    """Contains a list of documents with each document having two keys: 'text' and 'source'."""

    def __init__(
        self,
        pinecone_api_key: str,
        openai_api_key: str,
        index_name: str = "law-documents",
        openai_embeddings_model: str = "text-embedding-3-large",
        text_field: str = "text",
    ) -> None:
        self.pinecone_api_key = pinecone_api_key
        self.openai_api_key = openai_api_key
        self.openai_embeddings_model = openai_embeddings_model
        self.index_name = index_name
        self.text_field = text_field

        # Instances to be created
        self.Index = None
        self.Pinecone = None
        self.embeddings_model = None

        self.chunked_text = None

        self._load_index()
        self._create_embeddings_model()

    def _create_embeddings_model(self) -> None:
        """
        Creates an instance of OpenAIEmbeddings
        """
        self.embeddings_model = OpenAIEmbeddings(
            api_key=self.openai_api_key, model=self.openai_embeddings_model
        )

    def _load_index(self) -> None:
        """
        Creates a Pinecone index or loads it if it exists.
        """
        self.Pinecone = Pinecone(api_key=self.pinecone_api_key)
        self.Index = self.Pinecone.Index(self.index_name)

    def _process_pdf(self, files: List[str]) -> None:
        self.chunked_text = convert_to_text(files)

    def _check_document_exists(self) -> None:
        pass

    def upload_documents(self, files: List[str], batch_size: int = 100) -> None:
        """
        Uploads documents to Pinecone in batches.
        """
        self._process_pdf(files)

        for i in tqdm(
            range(0, len(self.chunked_text), batch_size), desc="Uploading batches"
        ):
            i_end = min(len(self.chunked_text), i + batch_size)
            batch = self.chunked_text[i:i_end]
            ids = [
                f"{x['source'].encode('ascii', 'ignore').decode()}-{index}"
                for index, x in enumerate(batch)
            ]
            texts = [x["text"] for x in batch]
            embeds = self.embeddings_model.embed_documents(texts)
            metadata = [
                {self.text_field: x["text"], "source": x["source"]} for x in batch
            ]
            for attempt in range(10):
                try:
                    self.Index.upsert(vectors=list(zip(ids, embeds, metadata)))
                    break
                except Exception as e:
                    if attempt == 9:
                        raise Exception(f"Failed to upsert after 10 attempts: {e}")
                    time.sleep(1)  # Wait a bit before retrying
