#!/usr/bin/env python3
"""Download LLaMA 2 7B Chat GGUF model from Hugging Face."""

import os
import sys
import shutil
from pathlib import Path

def download_model():
    """Download the LLaMA model."""
    print(' Starting LLaMA 2 7B Chat GGUF model download...')
    print('This may take 10-20 minutes depending on your internet speed.')
    print()
    
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print(' huggingface-hub not installed')
        sys.exit(1)
    
    models_dir = Path('/Users/kishanshirshikk/Downloads/tropic/backend/models')
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_filename = 'llama-2-7b-chat.Q4_K_M.gguf'
    local_model_path = models_dir / model_filename
    
    # If model already exists, skip download
    if local_model_path.exists():
        print(f' Model already exists at: {local_model_path}')
        print(f'   Size: {local_model_path.stat().st_size / (1024**3):.2f} GB')
        return
    
    try:
        # Download to HuggingFace cache
        print(' Downloading to cache first (this is normal)...')
        cache_path = hf_hub_download(
            repo_id='TheBloke/Llama-2-7B-chat-GGUF',
            filename=model_filename,
            cache_dir=None,  # Use default HuggingFace cache
        )
        
        print(f' Download complete!')
        print(f' Cache location: {cache_path}')
        
        # Copy to models directory
        print(f' Copying to {models_dir}...')
        shutil.copy2(cache_path, local_model_path)
        
        print()
        print(' Model is ready!')
        print(f' Location: {local_model_path}')
        print(f'   Size: {local_model_path.stat().st_size / (1024**3):.2f} GB')
        print()
        print(' Your backend/.env file has been pre-configured!')
        print('   Restart the backend server to use the model.')
        
    except KeyboardInterrupt:
        print(' Download cancelled by user')
        sys.exit(1)
    except Exception as e:
        print(f' Download failed: {e}')
        print()
        print('Alternative: Download manually from:')
        print('  https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF')
        print()
        print('Then place the file at:')
        print(f'  {local_model_path}')
        sys.exit(1)

if __name__ == '__main__':
    download_model()

