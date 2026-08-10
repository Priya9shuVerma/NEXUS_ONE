import logging
import os

from langchain_community.vectorstores import FAISS
from app.ai.embeddings import get_embeddings

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

VECTOR_PATH = os.path.join(
    BASE_DIR,
    "vector_db"
)


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local(VECTOR_PATH)

    logger.info("FAISS vector store saved")

    return vector_store



def load_vector_store():

    embeddings = get_embeddings()

    if not os.path.exists(VECTOR_PATH):
        raise FileNotFoundError("Vector store path does not exist.")

    logger.info("Loading FAISS vector store")

    vector_store = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store