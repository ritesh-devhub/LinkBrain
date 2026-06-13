import chromadb
import config 

client = chromadb.PersistentClient(path=config.PATH)

def get_collection():

    collection = client.get_or_create_collection(name=config.COLLECTION_NAME)

    return collection


def store_embedding(embedded_chunks):

    ids = [chunk['chunk_id'] for chunk in embedded_chunks]

    documents = [chunk['chunk_text'] for chunk in embedded_chunks]

    embeddings = [chunk['embedding'] for chunk in embedded_chunks]

    metadatas = [
        {
            'document_id': chunk['document_id'],
            'title': chunk['title'],
            'url': chunk['url'],
            'chunk_number': chunk['chunk_number'],
            'total_chunks': chunk['total_chunks'],'content_type': chunk['content_type']
        }
        for chunk in embedded_chunks
    ]

    collection = get_collection()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    # Need to write a return statement
    return 

