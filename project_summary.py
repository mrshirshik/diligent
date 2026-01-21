#!/usr/bin/env python3
"""
Project Summary and Verification Script
Displays the complete project structure and provides setup instructions
"""

import os
import json
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def get_tree_structure(path, prefix="", is_last=True, max_depth=4, current_depth=0):
    """Generate tree structure of directories"""
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return
    
    # Filter out common unwanted items
    skip_items = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.next', 
                  'dist', 'build', '.venv', 'venv', '.env', '*.pyc', '.DS_Store'}
    items = [i for i in items if not any(i.startswith(s.rstrip('*')) for s in skip_items)]
    
    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        item_path = os.path.join(path, item)
        
        connector = "└── " if is_last_item else "├── "
        print(f"{prefix}{connector}{item}")
        
        if os.path.isdir(item_path) and not item.startswith('.'):
            extension = "    " if is_last_item else "│   "
            get_tree_structure(item_path, prefix + extension, is_last_item, max_depth, current_depth + 1)

def main():
    project_root = "/Users/kishanshirshikk/Downloads/tropic"
    
    print_header("🤖 JARVIS - Personal AI Assistant")
    print("A self-hosted LLM-powered assistant with vector database integration")
    print("and a beautiful conversational UI.\n")
    
    # Project Statistics
    print_header("📊 Project Statistics")
    
    backend_files = len([f for f in Path(f"{project_root}/backend").glob("*.py")])
    frontend_files = len([f for f in Path(f"{project_root}/frontend/src").rglob("*.jsx")])
    docs = len([f for f in Path(project_root).glob("*.md")])
    
    print(f"Backend Python Files:  {backend_files}")
    print(f"Frontend React Files:  {frontend_files}")
    print(f"Documentation Pages:   {docs}")
    print(f"Configuration Files:   Multiple (.env, vite.config.js, etc.)")
    
    # Directory Structure
    print_header("📁 Directory Structure")
    print(f"{Path(project_root).name}/")
    get_tree_structure(project_root)
    
    # Key Features
    print_header("✨ Key Features")
    features = [
        "Self-hosted LLaMA 2 language model",
        "Pinecone vector database integration",
        "Semantic search and RAG (Retrieval Augmented Generation)",
        "Modern React-based chatbot UI",
        "Knowledge base management",
        "REST API with FastAPI",
        "Sentence-Transformers embeddings",
        "Multi-turn conversation support",
        "Source attribution and confidence scores"
    ]
    for i, feature in enumerate(features, 1):
        print(f"{i}. {feature}")
    
    # Technology Stack
    print_header("🛠️ Technology Stack")
    
    stacks = {
        "Backend": ["Python 3.9+", "FastAPI", "llama-cpp-python", "sentence-transformers", "Pinecone"],
        "Frontend": ["React 18", "Vite", "Tailwind CSS", "Axios", "Lucide Icons"],
        "Infrastructure": ["Pinecone (Vector DB)", "LLaMA 2 (LLM)", "Local storage"]
    }
    
    for category, techs in stacks.items():
        print(f"\n{category}:")
        for tech in techs:
            print(f"  • {tech}")
    
    # File Descriptions
    print_header("📝 Important Files")
    
    files_desc = {
        "README.md": "Project overview and features",
        "QUICKSTART.md": "Getting started guide",
        "API.md": "Complete API documentation",
        "DEPLOYMENT.md": "Production deployment guide",
        "ARCHITECTURE.md": "System design and architecture",
        "backend/main.py": "FastAPI application",
        "backend/config.py": "Configuration management",
        "frontend/src/App.jsx": "React root component",
        "frontend/src/api.js": "API client",
        "setup.sh": "Automated setup script",
        "start.sh": "Start services script",
        "populate_kb.py": "Sample data loader",
        "examples.py": "Advanced usage examples"
    }
    
    for file_path, desc in files_desc.items():
        print(f"• {file_path}")
        print(f"  → {desc}\n")
    
    # Setup Instructions
    print_header("🚀 Quick Start")
    
    steps = [
        ("1. Setup", "chmod +x setup.sh && ./setup.sh"),
        ("2. Configure", "Edit backend/.env with Pinecone credentials"),
        ("3. Download Model", "Get LLaMA 2 GGUF model to backend/models/"),
        ("4. Run", "./start.sh"),
        ("5. Access", "Open http://localhost:5173 in browser")
    ]
    
    for step, cmd in steps:
        print(f"{step}:")
        print(f"  $ {cmd}\n")
    
    # Next Steps
    print_header("📚 Next Steps")
    
    next_steps = [
        "Read QUICKSTART.md for detailed setup instructions",
        "Review API.md to understand available endpoints",
        "Check ARCHITECTURE.md to understand system design",
        "Run populate_kb.py to add sample knowledge",
        "Experiment with multi-turn conversations",
        "Customize LLM parameters in .env",
        "Deploy to production (see DEPLOYMENT.md)",
        "Extend with custom embeddings or LLM models"
    ]
    
    for i, step in enumerate(next_steps, 1):
        print(f"{i}. {step}")
    
    # System Requirements
    print_header("💻 System Requirements")
    
    requirements = {
        "Python": "3.9+",
        "Node.js": "16+",
        "RAM": "4GB minimum (8GB+ recommended)",
        "Disk": "10GB+ for models",
        "Internet": "Required for Pinecone",
        "OS": "macOS, Linux, or Windows"
    }
    
    for req, value in requirements.items():
        print(f"• {req}: {value}")
    
    # API Endpoints
    print_header("🔌 Core API Endpoints")
    
    endpoints = [
        ("POST", "/chat", "Send query and get response"),
        ("GET", "/health", "Check system status"),
        ("GET", "/knowledge", "Get all entries"),
        ("POST", "/knowledge", "Add new entry"),
        ("PUT", "/knowledge/{id}", "Update entry"),
        ("DELETE", "/knowledge/{id}", "Delete entry"),
        ("POST", "/search", "Search knowledge base")
    ]
    
    print(f"{'Method':<8} {'Endpoint':<20} {'Description':<30}")
    print("-" * 58)
    for method, endpoint, desc in endpoints:
        print(f"{method:<8} {endpoint:<20} {desc:<30}")
    
    # Environment Variables
    print_header("⚙️ Key Environment Variables")
    
    env_vars = {
        "PINECONE_API_KEY": "Your Pinecone API key",
        "PINECONE_INDEX_NAME": "Vector database index name",
        "LLM_MODEL_PATH": "Path to GGUF model file",
        "EMBEDDING_MODEL": "Hugging Face embedding model",
        "API_PORT": "Backend API port (default: 8000)",
        "CORS_ORIGINS": "Allowed frontend URLs"
    }
    
    for var, desc in env_vars.items():
        print(f"• {var}")
        print(f"  → {desc}\n")
    
    # Final Information
    print_header("ℹ️ Additional Information")
    
    print("Free Tier Resources:")
    print("• Pinecone: 1 free index, 1 million vectors")
    print("• HuggingFace Models: Free downloads")
    print("• Meta LLaMA 2: Open source, free to use")
    print()
    print("Documentation:")
    print("• Full README: README.md")
    print("• API Docs: API.md")
    print("• Deployment: DEPLOYMENT.md")
    print("• Architecture: ARCHITECTURE.md")
    print()
    print("Support:")
    print("• Check logs for errors")
    print("• Visit /docs for OpenAPI documentation")
    print("• Review examples.py for advanced usage")
    
    print_header("✅ Project Ready!")
    print("Your Personal AI Assistant is ready to deploy.")
    print("Start with: ./setup.sh && ./start.sh\n")

if __name__ == "__main__":
    main()
