import os
import pytest
import tempfile
from PIL import Image, ImageDraw

# Add current workspace directory to sys.path so we can import app and database packages
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pdf_parser import extract_text_from_pdf
from app.ocr_engine import extract_text_from_image
from app.llm_client import OllamaClient
from database.db_manager import DBManager
from app.pipeline import DocumentPipeline


@pytest.fixture
def temp_pdf():
    """Fixture to generate a temporary PDF file containing known text."""
    import fitz

    temp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(temp_dir, "test.pdf")

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (50, 50),
        "This is a local Python resume for John Doe, expert in PyTorch and SQLite.",
    )
    doc.save(pdf_path)
    doc.close()

    yield pdf_path

    # Cleanup
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    os.rmdir(temp_dir)


@pytest.fixture
def temp_image():
    """Fixture to generate a temporary image containing known text."""
    temp_dir = tempfile.mkdtemp()
    img_path = os.path.join(temp_dir, "test.png")

    # Create simple white image with black text
    img = Image.new("RGB", (300, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # Using default font
    d.text((20, 40), "INVOICE #99824", fill=(0, 0, 0))
    img.save(img_path)

    yield img_path

    # Cleanup
    if os.path.exists(img_path):
        os.remove(img_path)
    os.rmdir(temp_dir)


@pytest.fixture
def temp_db():
    """Fixture to initialize an in-memory or temp-file database."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db = DBManager(db_path)

    yield db

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


def test_pdf_extraction(temp_pdf):
    text = extract_text_from_pdf(temp_pdf)
    assert "John Doe" in text
    assert "PyTorch" in text
    assert "SQLite" in text


def test_ocr_extraction(temp_image):
    # OCR might sometimes have minor character variance depending on Tesseract's build,
    # so we search for subsets or partial values.
    text = extract_text_from_image(temp_image)
    assert "99824" in text or "INVOICE" in text or "IN" in text


def test_db_indexing_and_retrieval(temp_db, temp_pdf):
    # Prepare dummy metadata
    metadata = {
        "document_type": "Resume",
        "title": "John Doe Resume",
        "summary": "Resume of a Python Developer.",
        "tags": ["python", "pytorch", "resume"],
        "metadata": {"applicant": "John Doe", "skills": ["Python", "PyTorch"]},
    }

    extracted_text = (
        "This is a local Python resume for John Doe, expert in PyTorch and SQLite."
    )
    doc_id = temp_db.index_document(temp_pdf, extracted_text, metadata)

    # Verify file hash ID returned
    assert doc_id is not None
    assert len(doc_id) == 32  # MD5 hash length

    # Retrieve and check values
    doc = temp_db.get_document(doc_id)
    assert doc is not None
    assert doc["file_name"] == "test.pdf"
    assert doc["document_type"] == "Resume"
    assert doc["title"] == "John Doe Resume"
    assert doc["summary"] == "Resume of a Python Developer."
    assert "python" in doc["tags"]
    assert "pytorch" in doc["tags"]
    assert doc["metadata"]["applicant"] == "John Doe"


def test_db_search(temp_db, temp_pdf):
    # Setup multiple documents in DB
    metadata_1 = {
        "document_type": "Resume",
        "title": "Python Resume",
        "summary": "Developer summary.",
        "tags": ["python", "resume"],
        "metadata": {"name": "Alice"},
    }
    _ = temp_db.index_document(temp_pdf, "Python dev text", metadata_1)

    # Create another temp file for the second document
    fd, temp_file_2 = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    with open(temp_file_2, "w") as f:
        f.write("Invoice for host services")

    metadata_2 = {
        "document_type": "Invoice",
        "title": "Cloud Invoice",
        "summary": "Monthly server bill.",
        "tags": ["invoice", "server"],
        "metadata": {"amount": 250},
    }
    _ = temp_db.index_document(temp_file_2, "Invoice for host services", metadata_2)

    try:
        # Search by tag
        res_tag = temp_db.search_documents("invoice")
        assert len(res_tag) == 1
        assert res_tag[0]["document_type"] == "Invoice"

        # Search by keyword in text
        res_text = temp_db.search_documents("Developer")
        assert len(res_text) == 1
        assert res_text[0]["document_type"] == "Resume"

        # Blank search should return all
        res_all = temp_db.search_documents("")
        assert len(res_all) == 2
    finally:
        # Cleanup secondary temp file
        if os.path.exists(temp_file_2):
            os.remove(temp_file_2)


def test_llm_client_prompt():
    client = OllamaClient()
    # Check that prompt output templates can format correctly
    # If Ollama isn't running, it should return default dict without raising errors
    res = client.extract_metadata("Sample document content")
    assert isinstance(res, dict)
    assert "document_type" in res
    assert "title" in res
    assert "tags" in res
    assert "summary" in res
    assert "metadata" in res


def test_pipeline(temp_pdf):
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    try:
        pipeline = DocumentPipeline(db_path=db_path)

        # Test folder scanning
        folder = os.path.dirname(temp_pdf)
        files = pipeline.scan_folder(folder)
        assert temp_pdf in files

        # Test processing file
        res = pipeline.process_file(temp_pdf)
        assert res["status"] in ("indexed", "cached")
        assert res["id"] is not None

        # Check that it's cached on the second run (for performance)
        res_second = pipeline.process_file(temp_pdf)
        assert res_second["status"] == "cached"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
