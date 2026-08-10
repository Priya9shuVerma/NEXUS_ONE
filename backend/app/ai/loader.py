import os

import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    filename = os.path.basename(pdf_path)

    for index, chunk in enumerate(chunks):
        metadata = chunk.metadata or {}

        page = metadata.get("page")

        if isinstance(page, int):
            metadata["page"] = page
        else:
            metadata["page"] = 0

        metadata["source"] = filename
        metadata["filename"] = filename
        metadata["chunk_id"] = index + 1

        chunk.metadata = metadata

    logger.debug("Loaded PDF %s with %d pages and %d chunks", filename, len(documents), len(chunks))

    return chunks
