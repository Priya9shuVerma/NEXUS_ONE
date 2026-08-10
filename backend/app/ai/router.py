from app.ai.formatter import clean_response


def build_context(retriever, question: str):
    """
    Retrieve relevant documents and build context.
    """

    docs = retriever.invoke(question)

    if not docs:
        return "", []

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return context, docs


def format_answer(answer: str):
    """
    Clean AI response before sending to frontend.
    """

    return clean_response(answer)