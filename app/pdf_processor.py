import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extracts text content from a PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
