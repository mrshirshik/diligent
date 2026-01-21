#!/usr/bin/env python3
"""Download and setup LLaMA 2 7B Chat GGUF model."""

import sys
import os
from pathlib import Path

def main():
    models_dir = Path("/Users/kishanshirshikk/Downloads/tropic/backend/models")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_file = models_dir / "llama-2-7b-chat.Q4_K_M.gguf"
    
    if model_file.exists():
        size_gb = model_file.stat().st_size / (1024**3)
        print(f"✅ Model already exists!")
        print(f"📁 Location: {model_file}")
        print(f"📊 Size: {size_gb:.2f} GB")
        return 0
    
    print("🔄 Downloading LLaMA 2 7B Chat GGUF model...")
    print("⏱️  This will take 10-20 minutes depending on your internet speed")
    print()
    
    try:
        from huggingface_hub import snapshot_download
        import shutil
        
        print("⏳ Fetching model repository...")
        repo_path = snapshot_download(
            repo_id="TheBloke/Llama-2-7B-chat-GGUF",
            allow_patterns="llama-2-7b-chat.Q4_K_M.gguf"
        )
        
        print("🔍 Locating model file...")
        # Find the model file
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file == "llama-2-7b-chat.Q4_K_M.gguf":
                    src = Path(root) / file
                    size_gb = src.stat().st_size / (1024**3)
                    
                    print(f"✅ Found: {src}")
                    print(f"📊 Size: {size_gb:.2f} GB")
                    print()
                    print(f"📁 Copying to {model_file}...")
                    
                    shutil.copy2(src, model_file)
                    
                    final_size = model_file.stat().st_size / (1024**3)
                    print(f"✅ Model copied successfully!")
                    print(f"📊 Final size: {final_size:.2f} GB")
                    print()
                    print("✨ LLaMA model is ready!")
                    print()
                    print("📝 Configuration:")
                    print(f"   - Model path: ./models/llama-2-7b-chat.Q4_K_M.gguf")
                    print(f"   - Backend .env: Pre-configured ✓")
                    print()
                    print("🚀 Next steps:")
                    print("   1. Restart your backend server")
                    print("   2. The chat interface will use the local LLaMA model")
                    
                    return 0
        
        print("❌ Model file not found in repository")
        return 1
        
    except ImportError:
        print("❌ huggingface-hub not installed")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Download interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Alternative: Download manually from")
        print("   https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF")
        print()
        print(f"Then place at: {model_file}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
