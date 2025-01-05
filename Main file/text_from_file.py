#extract texts from file(pdf or doc)
import PyPDF2
from docx import Document
import re
import string
import io


# Extract text from PDF file-like object
def extract_text_from_pdf(uploaded_file):
    # Use io.BytesIO to wrap the uploaded file's binary data
    with io.BytesIO(uploaded_file.read()) as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            if page.extract_text():  # Check if text extraction is successful
                text += page.extract_text()
        # Clean up the extracted text
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Preserve paragraph breaks
        text = re.sub(r'(?<!\n)\n(?=\S)', ' ', text)  # Replace single newlines with space
        text = re.sub(r'\n', ' ', text)  # Remove remaining newlines
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text


#extract text from the doc file..
def extract_text_from_docx(uploaded_file):
    # Use io.BytesIO to handle the uploaded file's binary data
    with io.BytesIO(uploaded_file.read()) as docx_file:
        doc = Document(docx_file)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        # Join paragraphs into a single string
        text = '\n'.join(text)
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # Replace newlines followed by a lowercase letter with a space
        text = re.sub(r'(?<!\n)\n(?=\S)', ' ', text)
        # Remove other unnecessary newlines
        text = re.sub(r'\n', ' ', text)
        # Remove excess spaces
        text = re.sub(r'\s+', ' ', text).strip()
    return text