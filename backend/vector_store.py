from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from config import settings
from typing import List, Dict, Any, Tuple
import uuid

# Import embedding providers
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    LOCAL_AVAILABLE = True
except ImportError:
    LOCAL_AVAILABLE = False


class VectorStore:
    """Manages vector storage and retrieval with Qdrant."""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.embedding_provider = settings.embedding_provider.lower()
        self.collection_name = settings.qdrant_collection_name
        
        # Initialize embedding client based on provider
        # Lazy load the model to avoid memory issues on startup
        self.model = None
        self.cohere_client = None
        self.openai_client = None
        
        if self.embedding_provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("openai package required: pip install openai")
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            self.embedding_model = settings.embedding_model
        
        # Defer collection creation to runtime (avoid network/API calls at import time)
        # self._ensure_collection()
    
    def _load_local_model(self):
        """Lazy load the sentence-transformers model only when needed."""
        if self.embedding_provider == "local" and self.model is None:
            if not LOCAL_AVAILABLE:
                raise ImportError("sentence-transformers required: pip install sentence-transformers")
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except OSError as e:
                print(f"⚠️  Warning: Could not load local embedding model: {str(e)}")
                print("⚠️  Falling back to OpenAI or Cohere embeddings")
                return False
        return True
    
    def _ensure_collection(self):
        """Ensure collection exists in Qdrant."""
        try:
            self.client.get_collection(self.collection_name)
        except:
            # Collection doesn't exist, create it
            # Get embedding dimension by generating a sample embedding
            sample_embedding = self._get_embedding("sample text")
            embedding_size = len(sample_embedding)
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
            )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using configured provider."""
        if self.embedding_provider == "local":
            # Lazy load the model only when needed
            if not self._load_local_model():
                # Fallback to OpenAI
                if self.openai_client:
                    response = self.openai_client.embeddings.create(
                        input=text,
                        model=self.embedding_model
                    )
                    return response.data[0].embedding
                else:
                    raise RuntimeError("Cannot load local model and OpenAI not configured")
            embedding = self.model.encode(text)
            return embedding.tolist()
        elif self.embedding_provider == "cohere":
            try:
                response = self.cohere_client.embed(
                    texts=[text],
                    model=self.embedding_model,
                    input_type="search_document"
                )
                # Cohere returns embeddings in response.embeddings
                if hasattr(response, 'embeddings'):
                    emb = response.embeddings
                    if isinstance(emb, list) and len(emb) > 0:
                        return list(emb[0]) if not isinstance(emb[0], list) else emb[0]
                    elif hasattr(emb, '__iter__'):
                        return list(emb)
                return [0.0] * 1024
            except Exception as e:
                print(f"Cohere embedding error: {str(e)}")
                return [0.0] * 1024
        elif self.embedding_provider == "openai":
            # OpenAI
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        else:
            raise ValueError(f"Unknown embedding_provider: {self.embedding_provider}")
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Add documents to vector store."""
        points = []
        embedding_ids = []
        
        for doc in documents:
            # Generate embedding for document content
            embedding = self._get_embedding(doc["content"])
            embedding_id = str(uuid.uuid4())
            
            # Create point for Qdrant
            point = PointStruct(
                id=hash(embedding_id) % (10**8),  # Convert to positive int
                vector=embedding,
                payload={
                    "embedding_id": embedding_id,
                    "title": doc.get("title", ""),
                    "chapter": doc.get("chapter", ""),
                    "content": doc.get("content", ""),
                    "source_url": doc.get("source_url", ""),
                }
            )
            points.append(point)
            embedding_ids.append(embedding_id)
        
        # Ensure collection exists now that we have an embedding to infer size
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # Create collection using the embedding size from the first point
            if points:
                embedding_size = len(points[0].vector)
            else:
                embedding_size = len(self._get_embedding("sample text"))

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
            )

        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return embedding_ids
    
    def search_similar(self, query: str, limit: int = 5, 
                      score_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        # Get embedding for query
        query_embedding = self._get_embedding(query)
        
        # Search in Qdrant
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold,
        )
        
        # Format results
        results = []
        for result in search_results:
            results.append({
                "score": result.score,
                "content": result.payload.get("content", ""),
                "title": result.payload.get("title", ""),
                "chapter": result.payload.get("chapter", ""),
                "source_url": result.payload.get("source_url", ""),
                "embedding_id": result.payload.get("embedding_id", ""),
            })
        
        return results
    
    def search_by_selected_text(self, selected_text: str, 
                               limit: int = 3) -> List[Dict[str, Any]]:
        """Search for context around selected text."""
        return self.search_similar(selected_text, limit=limit, score_threshold=0.5)


# Global vector store instance
vector_store = VectorStore()
