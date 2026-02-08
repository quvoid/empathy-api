import hashlib
from cachetools import TTLCache
from src.core.config import get_settings
from src.core.sanitizer import Sanitizer
from src.core.llm import LLMClient
from src.models.schemas import TranslateRequest, TranslateResponse, Severity


class TranslatorService:
    """
    Orchestrates the error translation flow:
    1. Sanitize input
    2. Check cache
    3. Call LLM if cache miss
    4. Store in cache
    5. Return response
    """

    def __init__(self):
        settings = get_settings()
        self._cache = TTLCache(
            maxsize=settings.cache_max_size,
            ttl=settings.cache_ttl_seconds,
        )
        self._llm = LLMClient()

    def _generate_cache_key(self, request: TranslateRequest) -> str:
        """Generate a unique cache key from the request."""
        key_str = f"{request.raw_message}|{request.error_code or ''}|{request.tone.value}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def translate(self, request: TranslateRequest) -> TranslateResponse:
        """
        Translate a technical error into a user-friendly message.

        Args:
            request: The translation request containing the error details.

        Returns:
            A TranslateResponse with the friendly message.
        """
        # Sanitize inputs
        sanitized_message = Sanitizer.sanitize(request.raw_message)
        sanitized_context = Sanitizer.sanitize(request.user_context)

        # Check cache
        cache_key = self._generate_cache_key(request)
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            return TranslateResponse(**cached_data, cached=True)

        # Call LLM
        llm_response = self._llm.translate(
            raw_message=sanitized_message,
            user_context=sanitized_context,
            tone=request.tone.value,
        )

        # Validate and normalize severity
        severity_str = llm_response.get("severity", "error").lower()
        try:
            severity = Severity(severity_str)
        except ValueError:
            severity = Severity.ERROR

        response_data = {
            "title": llm_response.get("title", "Something went wrong"),
            "message": llm_response.get("message", "An unexpected issue occurred."),
            "action": llm_response.get("action", "Please try again later."),
            "severity": severity,
        }

        # Store in cache
        self._cache[cache_key] = response_data

        return TranslateResponse(**response_data, cached=False)


# Singleton instance
_translator_service: TranslatorService | None = None


def get_translator_service() -> TranslatorService:
    """Get or create the translator service singleton."""
    global _translator_service
    if _translator_service is None:
        _translator_service = TranslatorService()
    return _translator_service
