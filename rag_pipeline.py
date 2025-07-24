from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RAGPipeline:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = []

    def add_documents(self, docs):
        self.documents.extend(docs)
        self.embeddings = self.model.encode(self.documents, convert_to_tensor=True)

    def chunk_documents(self, text, chunk_size=512):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def embed_text(self, text):
        return self.model.encode(text, convert_to_tensor=True)

    def retrieve(self, query, top_k=5):
        query_embedding = self.embed_text(query)
        similarities = cosine_similarity(query_embedding, self.embeddings)
        top_k_indices = np.argsort(similarities[0])[-top_k:][::-1]
        return [(self.documents[i], similarities[0][i]) for i in top_k_indices]

    def generate_response(self, query):
        retrieved_docs = self.retrieve(query)
        # Here you would implement the logic to generate a response based on retrieved documents
        return retrieved_docs