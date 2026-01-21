"""Embedding Manager - Handles text embeddings using sentence transformers."""

import logging
from typing import List, Any
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manages text embeddings using sentence transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize Embedding Manager.

        Args:
            model_name: HuggingFace model name for embeddings
        """
        self.model_name = model_name
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the embedding model."""
        try:
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully!")

        except ImportError:
            logger.warning("sentence-transformers not installed. Install with: pip install sentence-transformers")
            self.model = None
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            self.model = None

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Input text to embed

        Returns:
            Embedding vector
        """
        if self.model is None:
            logger.warning("Embedding model not available, returning random vector")
            return np.random.rand(384).tolist()

        try:
            embedding: Any = self.model.encode(text, convert_to_tensor=False)
            # Handle different return types from sentence-transformers
            if isinstance(embedding, np.ndarray):
                return embedding.tolist()
            elif hasattr(embedding, 'tolist'):
                result = embedding.tolist()
                return result if isinstance(result[0], float) else [float(x) for row in result for x in (row if isinstance(row, list) else [row])]
            elif isinstance(embedding, list):
                return [float(x) if not isinstance(x, (int, float)) else x for x in embedding]
            else:
                return [float(x) for x in embedding]

        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            return np.random.rand(384).tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        if self.model is None:
            logger.warning("Embedding model not available, returning random vectors")
            return [np.random.rand(384).tolist() for _ in texts]

        try:
            embeddings: Any = self.model.encode(texts, convert_to_tensor=False)
            # Handle different return types from sentence-transformers
            if isinstance(embeddings, np.ndarray):
                return embeddings.tolist()
            elif hasattr(embeddings, 'tolist'):
                result = embeddings.tolist()
                return [[float(x) for x in row] if isinstance(row, list) else [float(embeddings[0])] for row in result]
            elif isinstance(embeddings, list):
                if embeddings and isinstance(embeddings[0], list):
                    return [[float(x) if not isinstance(x, (int, float)) else x for x in row] for row in embeddings]
                else:
                    return [[float(x) if not isinstance(x, (int, float)) else x for x in embeddings]]
            else:
                return [[float(x) for x in embeddings]]

        except Exception as e:
            logger.error(f"Error embedding texts: {e}")
            return [np.random.rand(384).tolist() for _ in texts]

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings."""
        if self.model is None:
            return 384  # Default dimension for all-MiniLM-L6-v2

        try:
            # Get dimension by embedding a test string
            test_embedding = self.embed_text("test")
            return len(test_embedding)
        except Exception:
            return 384
