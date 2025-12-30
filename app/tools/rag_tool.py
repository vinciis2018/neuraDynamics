from langchain_core.tools import tool
from app.vector_store.qdrant_index import ingest_and_get_retriever

# Global retriever instance to avoid re-ingesting on every call
# In a production app, this would be managed by dependency injection or a singleton pattern.
_RETRIEVER = None

def get_retriever():
    global _RETRIEVER
    if _RETRIEVER is None:
        _RETRIEVER = ingest_and_get_retriever()
    return _RETRIEVER

@tool
def ask_document(query: str) -> str:
    """
    Answers questions based on the provided Knowledge Base (PDF).
    Use this tool to answer ANY questions about history, cyclones, general knowledge, or specific topics found in the documents.
    If you don't know the answer, ALWAYS try this tool first.
    Args:
        query (str): The user's question.
    Returns:
        str: The retrieved answer or context.
    """
    retriever = get_retriever()
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found in the document."
    # Simple concatenation of retrieved context
    context = "\n\n".join([d.page_content for d in docs])
    print(context, ":::::::::: context")

    return context
