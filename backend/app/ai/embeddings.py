from langchain_community.embeddings import HuggingFaceEmbeddings


_embeddings = None


def get_embeddings():

    global _embeddings


    if _embeddings is None:

        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )


    return _embeddings