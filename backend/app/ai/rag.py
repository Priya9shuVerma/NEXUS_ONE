from app.ai.vectorstore import load_vector_store
from app.ai.llm import get_llm


def get_rag_chain():
    """
    Load FAISS and LLM.

    MMR retrieval is used instead of plain similarity retrieval
    so the context contains diverse but relevant chunks.
    """

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20,
            "lambda_mult": 0.7,
        },
    )

    llm = get_llm()

    return retriever, llm
