import sqlite3
import config

def create_tables():

    with sqlite3.connect(config.SQLITE_DB) as conn:

        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                url TEXT, 
                title TEXT,
                content_type TEXT,
                source_type TEXT,
                scraped_at TEXT,
                content TEXT,
                content_hash TEXT UNIQUE,
                content_length INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                document_id TEXT, 
                chunk_number INTEGER,
                total_chunks INTEGER,
                url TEXT,
                title TEXT,
                content_type TEXT,
                chunk_text TEXT,
                FOREIGN KEY (document_id)
                       REFERENCES documents(document_id)
            )
        """)

        conn.commit()

        print("\nTABLES CREATED SUCCESSFULLY\n")



def save_document(document):
    
    with sqlite3.connect(config.SQLITE_DB) as conn:

        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO documents (document_id, url, title, content_type, source_type, scraped_at, content, content_hash, content_length) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (
            document['document_id'],
            document['url'],
            document['title'],
            document['content_type'],
            document['source_type'],
            document['scraped_at'],
            document['content'],
            document['content_hash'],
            document['content_length']
            )
        )

        inserted = cursor.rowcount

        conn.commit()

        return inserted > 0



def save_chunks(chunks):
    
    with sqlite3.connect(config.SQLITE_DB) as conn:

        cursor = conn.cursor()

        for chunk in chunks:
            cursor.execute(
                "INSERT OR IGNORE INTO chunks (chunk_id, document_id, chunk_number, total_chunks, url, title, content_type, chunk_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                (chunk['chunk_id'],
                chunk['document_id'],
                chunk['chunk_number'],
                chunk['total_chunks'],
                chunk['url'],
                chunk['title'],
                chunk['content_type'],
                chunk['chunk_text']
                )
        )
        
        conn.commit()



def get_documents():
        
    with sqlite3.connect(config.SQLITE_DB) as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM documents")
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)



def get_chunks():
        
    with sqlite3.connect(config.SQLITE_DB) as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM chunks")
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
