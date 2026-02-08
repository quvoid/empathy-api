import re
from typing import Optional


class Sanitizer:
    """
    Strips sensitive information from error messages before sending to LLM.
    This prevents PII and secrets from leaking to external services.
    """

    # Patterns for common sensitive data
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    JWT_PATTERN = re.compile(r"eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*")
    API_KEY_PATTERN = re.compile(
        r"(?:api[_-]?key|apikey|secret|password|token|bearer)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{16,})['\"]?",
        re.IGNORECASE,
    )
    FILE_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\|/)(?:[^\s\\/:*?\"<>|]+[/\\])*[^\s\\/:*?\"<>|]+")
    UUID_PATTERN = re.compile(
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
    )

    REPLACEMENTS = {
        "email": "[EMAIL_REDACTED]",
        "ip": "[IP_REDACTED]",
        "jwt": "[TOKEN_REDACTED]",
        "api_key": "[SECRET_REDACTED]",
        "file_path": "[PATH_REDACTED]",
        "uuid": "[ID_REDACTED]",
    }

    @classmethod
    def sanitize(cls, text: Optional[str]) -> str:
        """
        Remove sensitive data from the input text.

        Args:
            text: The raw error message or context string.

        Returns:
            A sanitized string with sensitive data replaced.
        """
        if not text:
            return ""

        result = text

        # Apply patterns in order of specificity
        result = cls.JWT_PATTERN.sub(cls.REPLACEMENTS["jwt"], result)
        result = cls.API_KEY_PATTERN.sub(cls.REPLACEMENTS["api_key"], result)
        result = cls.EMAIL_PATTERN.sub(cls.REPLACEMENTS["email"], result)
        result = cls.IP_PATTERN.sub(cls.REPLACEMENTS["ip"], result)
        result = cls.UUID_PATTERN.sub(cls.REPLACEMENTS["uuid"], result)
        # File paths last as they can be noisy
        result = cls.FILE_PATH_PATTERN.sub(cls.REPLACEMENTS["file_path"], result)

        return result
