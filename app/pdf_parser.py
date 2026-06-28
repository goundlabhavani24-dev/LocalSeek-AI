import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF document.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        str: The concatenated raw text content of all pages.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at: {file_path}")
        
    text_content = []
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text_content.append(page_text)
        doc.close()
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF file {file_path}: {e}")
        
    return "\n".join(text_content)
