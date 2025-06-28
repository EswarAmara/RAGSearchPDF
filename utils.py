import os
from typing import List, Tuple
from PyPDF2 import PdfReader

def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def parse_txt(file_path: str) -> str:
    """Read text from a .txt file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into chunks of chunk_size tokens with overlap."""
    import tiktoken
    enc = tiktoken.get_encoding('cl100k_base')
    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk = enc.decode(tokens[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def get_file_extension(filename: str) -> str:
    """Get the file extension."""
    return os.path.splitext(filename)[1].lower() 