import config
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(config.EMBEDDING_MODEL)

def embed_document(chunk_data):

    chunk_texts = [
        chunk['chunk_text'] 
        for chunk in chunk_data
    ]

    embeddings = model.encode(chunk_texts)

    embedded_chunks = []

    for chunk, embedding in zip(chunk_data, embeddings):

        chunk['embedding'] = embedding.tolist()

        embedded_chunks.append(chunk)

    return embedded_chunks

def embed_query(query):

    embedded_query = model.encode(query)

    return embedded_query

