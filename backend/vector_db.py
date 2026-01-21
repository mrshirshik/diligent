"""Vector Database Manager - Handles Pinecone integration."""

import logging
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class VectorDBManager:
    """Manages Pinecone vector database operations."""

    def __init__(self, api_key: str, environment: str, index_name: str):
        """
        Initialize Vector DB Manager.

        Args:
            api_key: Pinecone API key
            environment: Pinecone environment
            index_name: Index name
        """
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.index = None
        self._initialize_pinecone()

    def _initialize_pinecone(self):
        """Initialize Pinecone connection."""
        if not self.api_key:
            logger.warning("Pinecone API key not configured")
            self.index = None
            return

        try:
            from pinecone import Pinecone  # type: ignore[import]

            # Initialize Pinecone client
            pc = Pinecone(api_key=self.api_key)

            # Get existing index
            try:
                self.index = pc.Index(self.index_name)
                logger.info(f"✅ Connected to Pinecone index: {self.index_name}")
            except Exception as e:
                # Index doesn't exist, create it
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                try:
                    pc.create_index(
                        name=self.index_name,
                        dimension=384,  # Dimension for all-MiniLM-L6-v2
                        metric="cosine",
                        spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
                    )
                    logger.info(f"✅ Index created successfully")
                    self.index = pc.Index(self.index_name)
                    logger.info(f"✅ Connected to new Pinecone index: {self.index_name}")
                except Exception as create_error:
                    logger.error(f"Failed to create index: {create_error}")
                    self.index = None

        except ImportError:
            logger.warning("⚠️  pinecone-client not installed. Install with: pip install pinecone-client[grpc]")
            self.index = None
        except Exception as e:
            logger.error(f"⚠️  Failed to initialize Pinecone: {e}")
            self.index = None

    def upsert_vectors(self, vectors: List[tuple], namespace: str = "knowledge") -> bool:
        """
        Upsert vectors to Pinecone.

        Args:
            vectors: List of (id, embedding, metadata) tuples
            namespace: Namespace for vectors

        Returns:
            Success status
        """
        if self.index is None:
            logger.warning("Pinecone index not available")
            return False

        try:
            self.index.upsert(vectors=vectors, namespace=namespace)
            logger.info(f"Upserted {len(vectors)} vectors to namespace {namespace}")
            return True

        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return False

    def search_vectors(
        self, query_embedding: List[float], top_k: int = 5, namespace: str = "knowledge"
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            namespace: Namespace to search in

        Returns:
            List of search results with metadata
        """
        if self.index is None:
            logger.warning("Pinecone index not available")
            return []

        try:
            results = self.index.query(
                vector=query_embedding, top_k=top_k, namespace=namespace, include_metadata=True
            )

            formatted_results = []
            for match in results.get("matches", []):
                formatted_results.append(
                    {
                        "id": match["id"],
                        "score": match["score"],
                        "metadata": match.get("metadata", {}),
                    }
                )

            return formatted_results

        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []

    def delete_vectors(self, ids: List[str], namespace: str = "knowledge") -> bool:
        """
        Delete vectors from Pinecone.

        Args:
            ids: List of vector IDs to delete
            namespace: Namespace to delete from

        Returns:
            Success status
        """
        if self.index is None:
            logger.warning("Pinecone index not available")
            return False

        try:
            self.index.delete(ids=ids, namespace=namespace)
            logger.info(f"Deleted {len(ids)} vectors from namespace {namespace}")
            return True

        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return False

    def is_available(self) -> bool:
        """Check if vector database is available."""
        return self.index is not None
