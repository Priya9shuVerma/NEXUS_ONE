from app.ai.document_loader import load_pdf, split_documents
from app.ai.vectorstore import create_vector_store


pdf_path = "data/sample.pdf"


documents = load_pdf(pdf_path)

chunks = split_documents(documents)

create_vector_store(chunks)
