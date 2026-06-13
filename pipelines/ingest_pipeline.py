from ingestion import extractor, chunker, embedder
from database import chroma_db, sqlite_storage


def ingest_url(url):

    sqlite_storage.create_tables()

    try:
        document = extractor.scrape(url)
    except Exception as e:
        return {
        "success": False,
        "error": str(e)
    }

    if not document:
        return {
        "success": False,
        "message": "Document Not Found, Try again with valid url !"
    }

    if "document_id" not in document:
        return document


    print(document)


    saved = sqlite_storage.save_document(document)

    if not saved:
        return {
                "success": False,
                "message": "Document already exists"
    }

    try:
        chunks = chunker.chunk_document(document)
    except Exception as e:
        return {
        "success": False,
        "error": str(e)
    }

    sqlite_storage.save_chunks(chunks)

    try:
        embed = embedder.embed_document(chunks)
    except Exception as e:
        return {
        "success": False,
        "error": str(e)
    }
    
    chroma_db.store_embedding(embed)

    return  {
    "success": True,
    "message": "Successfully added document",
    "title": document["title"]
    }
