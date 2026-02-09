class EmpathyError(Exception):
    """Base exception for Empathy API."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LLMProviderError(EmpathyError):
    """Raised when the LLM provider fails (e.g., API down)."""

    def __init__(self, details: str):
        super().__init__(f"LLM Provider Error: {details}", status_code=503)


class RateLimitExceededError(EmpathyError):
    """Raised when the LLM provider rate limit is hit."""

    def __init__(self):
        super().__init__("Rate limit exceeded. Please try again later.", status_code=429)


class InvalidRequestError(EmpathyError):
    """Raised when the input is invalid."""

    def __init__(self, details: str):
        super().__init__(f"Invalid Request: {details}", status_code=400)
