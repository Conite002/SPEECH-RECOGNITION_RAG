def query_vector_store(query, vector_store, k=2):
    """Retrieves the most relevant chunks for a query."""
    retriever = vector_store.as_retriever()
    return retriever.get_relevant_documents(query, k=k)

def build_context(relevant_chunks):
    """Combines retrieved chunks into a single context string."""
    return "\n\n".join([chunk.page_content for chunk in relevant_chunks])

def remove_duplicate_chunks(chunks):
    """Removes duplicate chunks."""
    seen = set()
    unique_chunks = []
    for chunk in chunks:
        if chunk.page_content not in seen:
            unique_chunks.append(chunk)
            seen.add(chunk.page_content)
    return unique_chunks

def extract_unique_sources(filtered_chunks):
    """Extracts unique sources from chunk metadata."""
    sources = []
    for chunk in filtered_chunks:
        source = chunk.metadata.get("title", "Unknown source")
        if source not in sources:
            sources.append(source)
    return sources
