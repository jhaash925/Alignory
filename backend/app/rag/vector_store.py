import chromadb
from sentence_transformers import SentenceTransformer

# initialize chroma client
client = chromadb.Client()

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# create collection
collection = client.get_or_create_collection(name="resume_collection")


def add_documents(text_chunks):
    """
    Store resume chunks into vector database
    """

    embeddings = model.encode(text_chunks)

    for i, chunk in enumerate(text_chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[str(i)]
        )


def search_documents(query):
    """
    Retrieve most relevant resume chunks
    """

    query_embedding = model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    return results["documents"][0]