import pytesseract
from PIL import Image
import os

# Robustly find Tesseract binary if it's not in the path already
try:
    # Run a quick check
    pytesseract.get_tesseract_version()
except pytesseract.TesseractNotFoundError:
    # Set potential standard homebrew paths
    for path in ['/opt/homebrew/bin/tesseract', '/usr/local/bin/tesseract']:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

def extract_text_from_image(file_path: str) -> str:
    """
    Extract text content from an image file using Tesseract OCR.
    
    Args:
        file_path (str): The path to the image file.
        
    Returns:
        str: The extracted text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found at: {file_path}")
        
    try:
        img = Image.open(file_path)
        # Convert to grayscale to improve Tesseract OCR accuracy
        img_gray = img.convert('L')
        text = pytesseract.image_to_string(img_gray)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to perform OCR on image {file_path}: {e}")
