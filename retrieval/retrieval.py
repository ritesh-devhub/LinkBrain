from database.chroma_db import get_collection
from ingestion.embedder import embed_query
import config


def retrieve_context(user_query):
    query_embedding = embed_query(user_query)

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding.tolist()], 
        n_results=config.TOP_K,
        include=[
        "documents",
        "metadatas",
        "distances"
        ])
    
    return build_context(results)


def build_context(results):

    if not results['documents'] or not results["documents"][0]:
        return None, []

    chunks = results['documents'][0]

    sources = results['metadatas'][0]

    context = ""

    for i, chunk in enumerate(chunks):

        context += f"[Chunk {i+1}]\n" + chunk + "\n"


    return context, sources

