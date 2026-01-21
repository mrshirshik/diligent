"""
Advanced usage examples for the Personal AI Assistant.
"""

# Example 1: Adding bulk knowledge from a text file
import requests
from typing import Dict, Any

def bulk_add_knowledge(file_path, category="general"):
    """Add multiple knowledge entries from a text file."""
    with open(file_path, 'r') as f:
        entries: list[Dict[str, Any]] = []
        current_entry: Dict[str, Any] = {}
        
        for line in f:
            line = line.strip()
            if line.startswith("TITLE:"):
                if current_entry:
                    entries.append(current_entry)
                current_entry = {"title": line.replace("TITLE:", "").strip()}
            elif line.startswith("CONTENT:"):
                current_entry["content"] = line.replace("CONTENT:", "").strip()
            elif line.startswith("TAGS:"):
                tags_str = line.replace("TAGS:", "").strip()
                current_entry["tags"] = [tag.strip() for tag in tags_str.split(",")]
                current_entry["category"] = category
        
        if current_entry:
            entries.append(current_entry)
        
        # Add all entries
        for entry in entries:
            response = requests.post(
                "http://localhost:8000/knowledge",
                json=entry
            )
            print(f"Added: {entry['title']}")


# Example 2: Multi-turn conversation
def multi_turn_conversation(queries):
    """Have a multi-turn conversation with context."""
    conversation_history = []
    
    for query in queries:
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "query": query,
                "conversation_history": conversation_history
            }
        )
        
        result = response.json()
        
        # Add to history
        conversation_history.append({
            "role": "user",
            "content": query
        })
        conversation_history.append({
            "role": "assistant",
            "content": result["response"]
        })
        
        print(f"\nUser: {query}")
        print(f"Assistant: {result['response']}")
        print(f"Confidence: {result['confidence']:.2%}")


# Example 3: Semantic search and analysis
def analyze_knowledge_base():
    """Analyze the knowledge base with different searches."""
    searches = [
        "Python programming",
        "database optimization",
        "API design",
        "architecture patterns"
    ]
    
    for search_query in searches:
        response = requests.post(
            "http://localhost:8000/search",
            json={"query": search_query, "top_k": 3}
        )
        
        results = response.json()
        print(f"\nSearch: '{search_query}'")
        print(f"Found {len(results)} results:")
        for result in results:
            print(f"  - {result['title']}")


# Example 4: Update knowledge entries programmatically
def update_knowledge_entries():
    """Update existing entries based on new information."""
    # Get all entries
    response = requests.get("http://localhost:8000/knowledge")
    entries = response.json()
    
    # Update specific entry
    if entries:
        entry = entries[0]
        updated_data = {
            "content": entry["content"] + "\n[Updated: Added new information]",
            "tags": entry.get("tags", []) + ["updated"]
        }
        
        response = requests.put(
            f"http://localhost:8000/knowledge/{entry['id']}",
            json=updated_data
        )
        print(f"Updated: {entry['title']}")


# Example 5: Performance monitoring
def monitor_system_health():
    """Monitor system health and component availability."""
    response = requests.get("http://localhost:8000/health")
    health = response.json()
    
    print("System Health Status:")
    print(f"  Status: {health['status']}")
    print(f"  LLM Available: {'✓' if health['llm_available'] else '✗'}")
    print(f"  Vector DB Available: {'✓' if health['vector_db_available'] else '✗'}")
    print(f"  Embedding Model Available: {'✓' if health['embedding_model_available'] else '✗'}")
    
    return all([
        health['llm_available'],
        health['vector_db_available'],
        health['embedding_model_available']
    ])


# Example 6: Integration with external data sources
def import_from_markdown(md_file):
    """Import knowledge entries from markdown files."""
    # import markdown  # Optional: markdown rendering not required
    from html.parser import HTMLParser
    
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Parse markdown and extract sections
    sections = content.split('\n## ')
    
    for section in sections[1:]:  # Skip header
        lines = section.split('\n', 1)
        title = lines[0]
        content = lines[1] if len(lines) > 1 else ""
        
        # Add as knowledge entry
        response = requests.post(
            "http://localhost:8000/knowledge",
            json={
                "title": title,
                "content": content,
                "category": "imported",
                "source": md_file
            }
        )
        print(f"Imported: {title}")


if __name__ == "__main__":
    print("Personal AI Assistant - Advanced Examples")
    print("=" * 40)
    
    # Example usage
    print("\n1. Checking system health...")
    monitor_system_health()
    
    print("\n2. Multi-turn conversation example...")
    queries = [
        "What is a virtual environment in Python?",
        "Why would I use one?",
        "How do I create one?"
    ]
    multi_turn_conversation(queries)
    
    print("\n3. Semantic search example...")
    analyze_knowledge_base()
