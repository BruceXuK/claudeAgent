import os
from config import CHUNK_SIZE, CHUNK_OVERLAP


def load_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return _load_pdf(filepath)
    elif ext in (".txt", ".md", ".markdown"):
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"不支持的文件格式: {ext}")


def _load_pdf(filepath: str) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(filepath)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            texts.append(text)
    return "\n".join(texts)


def chunk_text(text: str, source: str) -> list[dict]:
    chunks = []
    start = 0
    chunk_idx = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({
                "content": chunk,
                "source": source,
                "chunk_index": chunk_idx,
            })
        chunk_idx += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def load_docs(docs_dir: str) -> list[dict]:
    all_chunks = []
    for filename in sorted(os.listdir(docs_dir)):
        filepath = os.path.join(docs_dir, filename)
        if not os.path.isfile(filepath):
            continue
        ext = os.path.splitext(filename)[1].lower()
        if ext not in (".pdf", ".txt", ".md", ".markdown"):
            continue
        try:
            text = load_file(filepath)
            chunks = chunk_text(text, filename)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"  跳过 {filename}: {e}")
    return all_chunks
