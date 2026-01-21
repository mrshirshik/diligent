"""Knowledge Base Manager - Handles knowledge storage and retrieval."""

import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Manages knowledge base operations."""

    def __init__(self, file_path: str):
        """
        Initialize Knowledge Base.

        Args:
            file_path: Path to knowledge base JSON file
        """
        self.file_path = Path(file_path)
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base from file."""
        if self.file_path.exists():
            try:
                with open(self.file_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading knowledge base: {e}")
                return {"entries": []}
        return {"entries": []}

    def _save_knowledge_base(self) -> bool:
        """Save knowledge base to file."""
        try:
            # Create parent directories if needed
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w") as f:
                json.dump(self.knowledge_base, f, indent=2)
            return True

        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
            return False

    def add_entry(
        self,
        title: str,
        content: str,
        category: str = "general",
        tags: Optional[List[str]] = None,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add a knowledge entry.

        Args:
            title: Entry title
            content: Entry content
            category: Entry category
            tags: List of tags
            source: Source of the entry

        Returns:
            Created entry
        """
        entry_id = len(self.knowledge_base["entries"]) + 1
        entry = {
            "id": entry_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "source": source,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.knowledge_base["entries"].append(entry)
        self._save_knowledge_base()
        logger.info(f"Added knowledge entry: {title}")
        return entry

    def update_entry(self, entry_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a knowledge entry.

        Args:
            entry_id: Entry ID
            **kwargs: Fields to update

        Returns:
            Updated entry
        """
        for entry in self.knowledge_base["entries"]:
            if entry["id"] == entry_id:
                entry.update(kwargs)
                entry["updated_at"] = datetime.now().isoformat()
                self._save_knowledge_base()
                logger.info(f"Updated knowledge entry: {entry_id}")
                return entry

        logger.warning(f"Entry not found: {entry_id}")
        return None

    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete a knowledge entry.

        Args:
            entry_id: Entry ID

        Returns:
            Success status
        """
        initial_len = len(self.knowledge_base["entries"])
        self.knowledge_base["entries"] = [e for e in self.knowledge_base["entries"] if e["id"] != entry_id]

        if len(self.knowledge_base["entries"]) < initial_len:
            self._save_knowledge_base()
            logger.info(f"Deleted knowledge entry: {entry_id}")
            return True

        logger.warning(f"Entry not found: {entry_id}")
        return False

    def get_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a knowledge entry.

        Args:
            entry_id: Entry ID

        Returns:
            Entry or None
        """
        for entry in self.knowledge_base["entries"]:
            if entry["id"] == entry_id:
                return entry
        return None

    def search_entries(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search knowledge entries.

        Args:
            query: Search query
            category: Filter by category

        Returns:
            List of matching entries
        """
        results = []
        query_lower = query.lower()

        for entry in self.knowledge_base["entries"]:
            if category and entry.get("category") != category:
                continue

            if (
                query_lower in entry["title"].lower()
                or query_lower in entry["content"].lower()
                or any(query_lower in tag.lower() for tag in entry.get("tags", []))
            ):
                results.append(entry)

        return results

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Get all knowledge entries."""
        return self.knowledge_base.get("entries", [])

    def get_entries_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get entries by category."""
        return [e for e in self.knowledge_base["entries"] if e.get("category") == category]
