from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

def chunk_document(document):

    text = document['content']

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = config.CHUNK_SIZE,
        chunk_overlap = config.CHUNK_OVERLAP
    )

    chunks = splitter.split_text(text)

    total_chunks = len(chunks)

    chunk_data = []

    for i, chunk in enumerate(chunks, start=1):

        chunk_data.append({
            'chunk_id': f"{document['document_id']}_chunk_{i}",
            'document_id': document['document_id'],
            'chunk_number': i,
            'total_chunks': total_chunks,
            'url': document['url'],
            'title': document['title'],
            'content_type': document['content_type'],
            'chunk_text': chunk
        })

    return chunk_data

