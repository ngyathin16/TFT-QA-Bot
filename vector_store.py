import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Tuple
import logging
from openai import OpenAI
import tiktoken

logger = logging.getLogger(__name__)

class TFTVectorStore:
    """FAISS-based vector store for TFT Set 15 data"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.index = None
        self.documents = []
        self.embeddings = []
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using OpenAI's text-embedding-ada-002"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error getting embedding: {e}")
            raise
    
    def create_embeddings(self, documents: List[Dict]) -> List[List[float]]:
        """Create embeddings for all documents"""
        embeddings = []
        logger.info(f"Creating embeddings for {len(documents)} documents...")
        
        for i, doc in enumerate(documents):
            try:
                embedding = self.get_embedding(doc['content'])
                embeddings.append(embedding)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(documents)} documents")
                    
            except Exception as e:
                logger.error(f"Error creating embedding for document {i}: {e}")
                # Use zero vector as fallback
                embeddings.append([0.0] * 1536)  # OpenAI ada-002 embedding dimension
        
        logger.info("Finished creating embeddings")
        return embeddings
    
    def build_index(self, documents: List[Dict], embeddings: List[List[float]]):
        """Build FAISS index from embeddings"""
        if not embeddings:
            raise ValueError("No embeddings provided")
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings_array)
        
        # Create FAISS index
        dimension = embeddings_array.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.index.add(embeddings_array)
        
        self.documents = documents
        self.embeddings = embeddings
        
        logger.info(f"Built FAISS index with {len(documents)} documents")
    
    def search(self, query: str, k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar documents"""
        if not self.index:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        query_vector = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_vector)
        
        # Search
        scores, indices = self.index.search(query_vector, k)
        
        # Return results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(score)))
        
        return results
    
    def save_index(self, filepath: str):
        """Save FAISS index and documents to disk"""
        if not self.index:
            raise ValueError("No index to save")
        
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.faiss")
        
        # Save documents
        with open(f"{filepath}.pkl", 'wb') as f:
            pickle.dump(self.documents, f)
        
        logger.info(f"Saved index to {filepath}")
    
    def load_index(self, filepath: str):
        """Load FAISS index and documents from disk"""
        # Load FAISS index
        self.index = faiss.read_index(f"{filepath}.faiss")
        
        # Load documents
        with open(f"{filepath}.pkl", 'rb') as f:
            self.documents = pickle.load(f)
        
        logger.info(f"Loaded index from {filepath} with {len(self.documents)} documents")
    
    def get_relevant_context(self, query: str, k: int = 3) -> str:
        """Get relevant context for a query"""
        results = self.search(query, k)
        
        context = ""
        for i, (doc, score) in enumerate(results):
            context += f"Document {i+1} (Relevance: {score:.3f}):\n{doc['content']}\n\n"
        
        return context.strip()
    
    def search_by_pattern(self, pattern: str) -> List[Dict]:
        """Search for documents containing a specific pattern"""
        matching_docs = []
        for doc in self.documents:
            if pattern.lower() in doc.get('content', '').lower():
                matching_docs.append(doc)
        return matching_docs
    
    def index_exists(self, filepath: str) -> bool:
        """Check if index files exist"""
        return os.path.exists(f"{filepath}.faiss") and os.path.exists(f"{filepath}.pkl")

if __name__ == "__main__":
    # Test the vector store
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY in your .env file")
        exit(1)
    
    # Test with sample data
    sample_docs = [
        {
            'content': 'Trait: Luchador - Luchadors gain bonus Attack Damage and can cleanse negative effects.',
            'metadata': {'type': 'trait', 'name': 'Luchador'}
        },
        {
            'content': 'Item: Infinity Edge - Provides critical strike chance and damage.',
            'metadata': {'type': 'item', 'name': 'Infinity Edge'}
        }
    ]
    
    vector_store = TFTVectorStore(api_key)
    embeddings = vector_store.create_embeddings(sample_docs)
    vector_store.build_index(sample_docs, embeddings)
    
    # Test search
    results = vector_store.search("What does Luchador do?")
    print("Search results:")
    for doc, score in results:
        print(f"Score: {score:.3f} - {doc['content'][:100]}...") 