"""LLM Manager - Handles local LLaMA model loading and inference."""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class LLMManager:
    """Manages LLaMA model loading and inference."""

    def __init__(self, model_path: str, context_window: int = 2048, max_tokens: int = 512, temperature: float = 0.7):
        """
        Initialize LLM Manager.

        Args:
            model_path: Path to the GGUF model file
            context_window: Context window size
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        """
        self.model_path = model_path
        self.context_window = context_window
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the LLaMA model."""
        try:
            # Import at function level to handle missing dependency gracefully
            try:
                from llama_cpp import Llama  # type: ignore[import]
            except ImportError:
                logger.warning(
                    "llama-cpp-python not installed. Install with: "
                    "pip install llama-cpp-python"
                )
                self.model = None
                return

            if not os.path.exists(self.model_path):
                logger.warning(
                    f"Model not found at {self.model_path}. "
                    "Please download a GGUF format model from: https://huggingface.co/TheBloke"
                )
                self.model = None
                return

            logger.info(f"Loading LLaMA model from {self.model_path}...")
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=self.context_window,
                n_threads=os.cpu_count() or 4,
                f16_kv=True,
                verbose=False,
            )
            logger.info("Model loaded successfully!")

        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            self.model = None

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate response from the model.

        Args:
            prompt: User query
            system_prompt: System prompt for context

        Returns:
            Model response
        """
        if self.model is None:
            return (
                "LLM model not available. Please ensure the model file is properly configured. "
                "For development, you can use a mock response or connect to an API-based LLM."
            )

        try:
            # Format the prompt with system message if provided
            if system_prompt:
                full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
            else:
                full_prompt = prompt

            # Generate response
            response = self.model(
                full_prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=0.9,
                stop=["User:", "System:"],
            )

            # Handle both dict and streaming responses
            if isinstance(response, dict):
                return response["choices"][0]["text"].strip()
            else:
                # For streaming responses, collect all chunks
                text = ""
                for chunk in response:
                    if "choices" in chunk and chunk["choices"]:
                        delta = chunk["choices"][0].get("text", "")
                        if delta:
                            text += delta
                return text.strip()

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error while processing your request."

    def is_available(self) -> bool:
        """Check if the model is available."""
        return self.model is not None
