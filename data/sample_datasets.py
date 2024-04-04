import time

import pinecone
from datasets import load_dataset

dataset = load_dataset(
    "jamescalam/llama-2-arxiv-papers-chunked",
    split="train"
)
# create pinecone instance
pinecone.init(api_key="251511d1-6f9d-477d-96be-785aa6249b0c")

index_name = "llama-2-rag"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        index_name,
        dimension=1536, # size of the vectors. Must be alligned and compatible with the embedding model
        metric="cosine"
    )
    
    while not pinecone.describe_index(index_name).status["ready"]:
        time.sleep(1)