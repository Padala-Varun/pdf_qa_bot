import fitz  # PyMuPDF
from docx import Document

def load_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def load_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def load_txt(file):
    return file.read().decode("utf-8")
