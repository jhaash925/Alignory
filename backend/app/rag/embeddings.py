from sentence_transformers import SentenceTransformer

# Load embedding model (runs locally, no API needed)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text_chunks):
    """
    Convert a list of text chunks into vector embeddings.
    """
    embeddings = model.encode(text_chunks)

    return embeddings