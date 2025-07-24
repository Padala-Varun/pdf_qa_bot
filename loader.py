import os
from PyPDF2 import PdfReader
from docx import Document

def load_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def load_docx(file_path):
    text = ""
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

def load_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        return load_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return load_docx(file_path)
    elif file_extension.lower() == '.txt':
        return load_txt(file_path)
    else:
        raise ValueError("Unsupported file format: {}".format(file_extension))