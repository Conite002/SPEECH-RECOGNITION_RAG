def chunk_text(text, max_length=200, overlap=50):
    """
    Splits text into chunks with overlap.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_length - overlap):
        chunks.append(" ".join(words[i:i + max_length]))
    return chunks

