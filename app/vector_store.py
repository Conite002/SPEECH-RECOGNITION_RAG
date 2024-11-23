from langchain_chroma import Chroma
from langchain_core.documents import Document
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from uuid import uuid4

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
embedding_model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size())
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    clamp = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / clamp

class CustomEmbeddingFunction:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def embed_documents(self, texts):
        """
        Fonction utilisée pour générer des embeddings pour une liste de textes.
        """
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, max_length=200, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings.tolist()

    def embed_query(self, text):
        """
        Fonction utilisée pour générer un embedding pour une seule requête.
        """
        return self.embed_documents([text])[0]

def sanitize_metadata(metadata):
    """
    Converts complex metadata into simple types compatible with ChromaDB.
    Args:
        metadata (dict): Original metadata.
    Returns:
        dict: Sanitized metadata.
    """
    sanitized = {}
    for key, value in metadata.items():
        if isinstance(value, (list, dict)):
            sanitized[key] = str(value)  # Convert lists/dicts to strings
        else:
            sanitized[key] = value
    return sanitized

def add_to_vector_store(vector_store, title, chunks, metadata):
    """
    Adds chunks to the vector store with sanitized metadata.
    """
    sanitized_metadata = sanitize_metadata(metadata)
    documents = [
        Document(
            id=str(uuid4()),
            page_content=chunk,
            metadata={**sanitized_metadata, "chunk_title": title}
        )
        for chunk in chunks
    ]
    vector_store.add_documents(documents=documents)

embedding_function = CustomEmbeddingFunction(model=embedding_model, tokenizer=tokenizer)



def init_vector_store(persist_directory):
    """Initializes the ChromaDB vector store."""
    return Chroma(
        collection_name="articles",
        embedding_function=embedding_function,
        persist_directory=persist_directory
    )

