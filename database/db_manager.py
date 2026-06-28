import sqlite3
import json
import hashlib
import os


class DBManager:
    """
    Database Manager class using SQLite to store document index and metadata.
    """

    def __init__(self, db_path: str = "database/localseek.db"):
        # Resolve absolute path to make sure it functions from any directory
        if not os.path.isabs(db_path):
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(current_dir, db_path)
        else:
            self.db_path = db_path

        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            # Create documents table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    file_path TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    title TEXT,
                    summary TEXT,
                    raw_text TEXT,
                    structured_metadata TEXT,
                    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Create document_tags table for relational tag queries
            conn.execute("""
                CREATE TABLE IF NOT EXISTS document_tags (
                    document_id TEXT,
                    tag TEXT,
                    FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE,
                    PRIMARY KEY (document_id, tag)
                )
            """)
            conn.commit()

    def compute_file_hash(self, file_path: str) -> str:
        """
        Compute MD5 hash of a file to uniquely identify it.
        """
        hash_md5 = hashlib.md5(usedforsecurity=False)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def index_document(
        self, file_path: str, extracted_text: str, metadata: dict
    ) -> str:
        """
        Index a document into the database. If it already exists (same hash), updates it.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        doc_id = self.compute_file_hash(file_path)
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1].lstrip(".").lower()

        doc_type = metadata.get("document_type", "Other")
        title = metadata.get("title", file_name)
        summary = metadata.get("summary", "")
        tags = metadata.get("tags", [])
        struct_metadata_str = json.dumps(metadata.get("metadata", {}))

        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO documents (
                    id, file_path, file_name, file_type, document_type, title, summary, raw_text, structured_metadata, indexed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
                (
                    doc_id,
                    file_path,
                    file_name,
                    file_type,
                    doc_type,
                    title,
                    summary,
                    extracted_text,
                    struct_metadata_str,
                ),
            )

            # Clear existing tags for this doc_id
            conn.execute("DELETE FROM document_tags WHERE document_id = ?", (doc_id,))

            # Insert tags
            for tag in tags:
                if tag.strip():
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO document_tags (document_id, tag) VALUES (?, ?)
                    """,
                        (doc_id, tag.strip().lower()),
                    )

            conn.commit()
        return doc_id

    def get_document(self, doc_id: str) -> dict:
        """
        Retrieve a single document and its tags by doc ID.
        """
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM documents WHERE id = ?", (doc_id,)
            ).fetchone()
            if row:
                doc = dict(row)
                doc["metadata"] = json.loads(doc.get("structured_metadata") or "{}")
                tag_rows = conn.execute(
                    "SELECT tag FROM document_tags WHERE document_id = ?", (doc_id,)
                ).fetchall()
                doc["tags"] = [t["tag"] for t in tag_rows]
                return doc
        return {}

    def search_documents(self, query: str) -> list:
        """
        Perform a flexible keyword and tag search over the indexed documents.
        """
        conn = self.get_connection()
        query = query.strip().lower()
        if not query:
            rows = conn.execute(
                "SELECT * FROM documents ORDER BY indexed_at DESC"
            ).fetchall()
        else:
            search_pattern = f"%{query}%"
            rows = conn.execute(
                """
                SELECT DISTINCT d.* FROM documents d
                LEFT JOIN document_tags t ON d.id = t.document_id
                WHERE LOWER(d.title) LIKE ?
                   OR LOWER(d.summary) LIKE ?
                   OR LOWER(d.raw_text) LIKE ?
                   OR LOWER(d.document_type) LIKE ?
                   OR LOWER(t.tag) LIKE ?
                ORDER BY d.indexed_at DESC
            """,
                (
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    search_pattern,
                ),
            ).fetchall()

        results = []
        for row in rows:
            doc = dict(row)
            doc_id = doc["id"]
            doc["metadata"] = json.loads(doc.get("structured_metadata") or "{}")
            tag_rows = conn.execute(
                "SELECT tag FROM document_tags WHERE document_id = ?", (doc_id,)
            ).fetchall()
            doc["tags"] = [t["tag"] for t in tag_rows]
            results.append(doc)

        conn.close()
        return results

    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document and its tags.
        """
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            conn.commit()
            return cursor.rowcount > 0
