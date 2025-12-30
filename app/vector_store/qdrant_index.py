import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.vectorstores import VectorStoreRetriever
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

DATA_PATH = "data/knowledge_base.pdf"
COLLECTION_NAME = "pdf_collection"

def get_vector_store():
    # Helper to get existing store (not used in main ingestion flow but good to have)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    client = QdrantClient(location=":memory:")
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

def ingest_and_get_retriever() -> VectorStoreRetriever:
    """
    Ingests the PDF and returns a retriever. 
    """
    try:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"{DATA_PATH} not found.")

        loader = PyPDFLoader(DATA_PATH)
        docs = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        
        embeddings = OpenAIEmbeddings()
        
        # Explicit Client
        client = QdrantClient(location=":memory:")
        
        # Explicit Collection Creation
        # text-embedding-3-small is 1536 dims
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        
        # Explicit Vector Store
        qdrant = QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding=embeddings,
        )
        
        qdrant.add_documents(chunks)
        
        return qdrant.as_retriever()
    except Exception as e:
        print(f"Error ingesting PDF: {e}")
        raise
