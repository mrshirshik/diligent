"""Sample knowledge entries to populate the knowledge base."""

sample_entries = [
    {
        "title": "Python Virtual Environments",
        "content": "Virtual environments are isolated Python environments that allow you to install packages for a specific project without affecting the system Python or other projects. Create one with 'python -m venv venv' and activate it with 'source venv/bin/activate' on Unix or 'venv\\Scripts\\activate' on Windows.",
        "category": "technical",
        "tags": ["python", "best-practices", "development"],
        "source": "Python Docs"
    },
    {
        "title": "REST API Best Practices",
        "content": "RESTful APIs should use appropriate HTTP methods (GET for retrieval, POST for creation, PUT for updates, DELETE for removal), return proper status codes, use meaningful URLs, implement versioning, document endpoints, and follow consistent naming conventions.",
        "category": "technical",
        "tags": ["api", "rest", "best-practices"],
        "source": "Web Development Guide"
    },
    {
        "title": "Git Workflow",
        "content": "A typical Git workflow involves creating a feature branch from main, making commits with meaningful messages, pushing to remote, creating a pull request for code review, and merging after approval. Always keep your main branch stable and deployable.",
        "category": "technical",
        "tags": ["git", "version-control", "collaboration"],
        "source": "Git Documentation"
    },
    {
        "title": "Database Indexing",
        "content": "Database indexes improve query performance by creating data structures that allow faster lookup. Common indexes include primary keys, unique indexes, and composite indexes. However, indexes slow down write operations and consume disk space, so they should be used strategically.",
        "category": "technical",
        "tags": ["database", "performance", "optimization"],
        "source": "Database Design"
    },
    {
        "title": "Microservices Architecture",
        "content": "Microservices decompose applications into small, independent services that communicate via APIs. Benefits include scalability and independent deployment, but challenges include complexity, network latency, and data consistency issues that require careful design patterns.",
        "category": "technical",
        "tags": ["architecture", "microservices", "design-patterns"],
        "source": "Software Architecture"
    }
]

if __name__ == "__main__":
    import sys
    import os
    from typing import Any, Type, Optional
    
    # Get the backend directory path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_path)
    
    # Now import
    KnowledgeBase: Optional[Type[Any]] = None
    kb: Optional[Any] = None
    try:
        from knowledge_base import KnowledgeBase as KB  # type: ignore[import]
        KnowledgeBase = KB
    except ImportError:
        # Fallback: Try importing from current directory structure
        import importlib.util
        spec = importlib.util.spec_from_file_location("knowledge_base", os.path.join(backend_path, "knowledge_base.py"))
        if spec and spec.loader:
            knowledge_base_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(knowledge_base_module)
            KnowledgeBase = knowledge_base_module.KnowledgeBase  # type: ignore[attr-defined]

    if KnowledgeBase:
        kb = KnowledgeBase('./data/knowledge_base.json')

        print("Populating knowledge base with sample entries...")
        for entry in sample_entries:
            kb.add_entry(**entry)  # type: ignore[union-attr]
            print(f"✓ Added: {entry['title']}")

        print(f"\nTotal entries: {len(kb.get_all_entries())}")  # type: ignore[union-attr]
    else:
        print("Error: Could not import KnowledgeBase module")
