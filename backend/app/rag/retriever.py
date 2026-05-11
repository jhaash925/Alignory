from app.utils.text_loader import load_resume_text
from app.rag.vector_store import add_documents, search_documents


def prepare_resume_database():
    """
    Load resume knowledge and store it in vector database
    """

    text = load_resume_text()

    # simple chunking
    chunks = text.split("\n\n")

    # store in vector DB
    add_documents(chunks)


def retrieve_relevant_experience(job_description):
    """
    Retrieve relevant resume chunks for a given job description
    """

    results = search_documents(job_description)

    return results