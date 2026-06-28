import os
from app.pdf_parser import extract_text_from_pdf
from app.ocr_engine import extract_text_from_image
from app.llm_client import OllamaClient
from database.db_manager import DBManager


class DocumentPipeline:
    """
    Orchestration pipeline to manage file discovery, text extraction,
    LLM metadata generation, and database storage.
    """

    def __init__(
        self,
        db_path: str = "database/localseek.db",
        ollama_host: str = "http://localhost:11434",
        model: str = "llama3.2",
    ):
        self.db = DBManager(db_path)
        self.llm = OllamaClient(ollama_host, model)

    def scan_folder(self, folder_path: str) -> list:
        """
        Scan a folder recursively for supported document files.
        """
        supported_extensions = (".pdf", ".png", ".jpg", ".jpeg", ".txt")
        found_files: list[str] = []
        if not os.path.exists(folder_path):
            return found_files

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    found_files.append(os.path.join(root, file))
        return found_files

    def process_file(self, file_path: str, force_reindex: bool = False) -> dict:
        """
        Process a single file: extract text, generate structured LLM metadata, and index in DB.
        If file hash matches an existing record and force_reindex is False, returns the cached record.

        Args:
            file_path (str): The absolute path to the file.
            force_reindex (bool): If True, re-runs parsing and LLM inference.

        Returns:
            dict: Status summary containing the document data.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # 1. Compute hash and check cache (FTS database)
        doc_id = self.db.compute_file_hash(file_path)
        existing_doc = self.db.get_document(doc_id)
        if existing_doc and not force_reindex:
            return {"id": doc_id, "status": "cached", "document": existing_doc}

        # 2. Extract raw text depending on extension
        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_name)[1].lower()
        extracted_text = ""

        try:
            if ext == ".pdf":
                extracted_text = extract_text_from_pdf(file_path)
            elif ext in (".png", ".jpg", ".jpeg"):
                extracted_text = extract_text_from_image(file_path)
            elif ext == ".txt":
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_text = f.read()
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        except Exception as e:
            return {
                "id": doc_id,
                "status": "error",
                "error": f"Extraction failed: {str(e)}",
            }

        if not extracted_text.strip():
            extracted_text = "[No readable text content extracted from this document.]"

        # 3. Generate structured metadata via local Llama 3.2
        metadata = self.llm.extract_metadata(extracted_text)

        # 4. Index in database
        self.db.index_document(file_path, extracted_text, metadata)

        # 5. Retrieve fresh copy of the record
        indexed_doc = self.db.get_document(doc_id)

        return {"id": doc_id, "status": "indexed", "document": indexed_doc}
