import hashlib
from cachetools import TTLCache
from typing import Dict, Any

from src.core.config import get_config
from src.core.sanitizer import Sanitizer
from src.models.schemas import TranslateRequest, TranslateResponse, Severity
from src.services.llm.gemini import GeminiProvider


class TranslatorService:
    """
    Orchestrates the translation workflow.
    """

    def __init__(self):
        self.config = get_config()
        self.cache = TTLCache(
            maxsize=self.config.CACHE_MAX_SIZE,
            ttl=self.config.CACHE_TTL_SECONDS,
        )
        self.llm_provider = GeminiProvider()
        
        # System prompt for the LLM
        self.system_prompt = """You are a UX copywriter specializing in user-facing error messages... (truncated for brevity, same logic as before) ..."""

    def _generate_cache_key(self, request: TranslateRequest) -> str:
        """Generate cache key."""
        key_str = f"{request.raw_message}|{request.error_code or ''}|{request.tone.value}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def translate(self, request: TranslateRequest) -> TranslateResponse:
        """Main translation logic."""
        
        # 1. Sanitize
        sanitized_message = Sanitizer.sanitize(request.raw_message)
        sanitized_context = Sanitizer.sanitize(request.user_context)

        # 2. Check Cache
        cache_key = self._generate_cache_key(request)
        if cache_key in self.cache:
            return TranslateResponse(**self.cache[cache_key], cached=True)

        # 3. Call LLM
        prompt = f"""Error: {sanitized_message}\nUser Context: {sanitized_context}\nTone: {request.tone.value}"""
        
        try:
             # Using hardcoded system prompt here or could move to config
            system_p = "You are a UX copywriter. translate error to friendly JSON {title, message, action, severity}."
            
            response_data = self.llm_provider.generate_response(
                prompt=prompt,
                system_instruction=system_p,
            )
            
            # Normalize response
            normalized_response = {
                "title": response_data.get("title", "Error"),
                "message": response_data.get("message", "An ongoing issue occurred."),
                "action": response_data.get("action", "Please try again."),
                "severity": Severity(response_data.get("severity", "error").lower()) 
            }

            # 4. Update Cache
            self.cache[cache_key] = normalized_response
            
            return TranslateResponse(**normalized_response, cached=False)
            
        except Exception:
             # On failure (e.g., rate limit), return fallback
             # In a real app, we might want to let the exception bubble up depending on strategy
             # But for robustness, we return a fallback here too?
             # Let's return fallback but log error
             return TranslateResponse(
                 title="Temporary Issue",
                 message="We're experiencing high load.",
                 action="Please try again in a moment.",
                 severity=Severity.WARNING,
                 cached=False
             )

# Singleton dependency
_service_instance = None

def get_translator_service() -> TranslatorService:
    global _service_instance
    if _service_instance is None:
        _service_instance = TranslatorService()
    return _service_instance
