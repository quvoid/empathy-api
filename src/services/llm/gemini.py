import google.generativeai as genai
import json
import time
from typing import Dict, Any

from src.core.config import get_config
from src.core.exceptions import LLMProviderError, RateLimitExceededError
from src.services.llm.base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini implementation of the LLM provider."""

    def __init__(self):
        self.config = get_config()
        try:
            genai.configure(api_key=self.config.GEMINI_API_KEY)
            # Use fallback model if main fails? For now just use configured model.
            self.model_name = self.config.GEMINI_MODEL
        except Exception as e:
            raise LLMProviderError(f"Failed to configure Gemini: {str(e)}")

    def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        config: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Generate response using Gemini with retry logic."""
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        # Use simple model instantiation for now as it's most reliable across versions
        model = genai.GenerativeModel("gemini-pro") 

        for attempt in range(3):
            try:
                response = model.generate_content(full_prompt)
                
                 # Clean response text
                text = response.text.strip()
                if text.startswith("```"):
                    lines = text.split("\n")
                    text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
                    text = text.rstrip("`").strip()
                
                return json.loads(text)

            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    time.sleep((attempt + 1) * 2) # Exponential backoff
                    continue
                # If it's a JSON parse error, maybe retry? 
                # For now, let's just log and raise provider error
                raise LLMProviderError(f"Gemini API failure: {str(e)}")

        raise RateLimitExceededError()
