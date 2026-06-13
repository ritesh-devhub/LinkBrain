import sqlite3
import config



def get_documents():
    """Return all saved documents, newest first."""
    try:
        with sqlite3.connect(config.SQLITE_DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT document_id, url, title, content_type, scraped_at, content_length "
                "FROM documents ORDER BY scraped_at DESC"
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        return []
    

def get_stats():
    """Return aggregate counts from the knowledge base."""
    try:
        with sqlite3.connect(config.SQLITE_DB) as conn:
            doc_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]

            return {"documents": doc_count, "chunks": chunk_count}
    except Exception:
        return {"documents": 0, "chunks": 0}



def get_latest_document():
    try:
        with sqlite3.connect(config.SQLITE_DB) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                """
                SELECT document_id,
                       url,
                       title,
                       content_type,
                       scraped_at
                FROM documents
                ORDER BY scraped_at DESC
                LIMIT 1
                """
            ).fetchone()

            return dict(row) if row else None

    except Exception:
        return None
