import requests
from typing import Optional, Dict


class EmpathyClient:
    """
    Client for the Empathy API.
    Translates technical errors into human-friendly messages.
    """

    def __init__(self, api_url: str = "http://localhost:8000"):
        """
        Initialize the client.

        Args:
            api_url: The URL of the Empathy API server.
        """
        self.api_url = api_url.rstrip("/")

    def translate(
        self,
        error: Exception | str,
        user_context: str = "",
        tone: str = "helpful",
    ) -> Dict[str, str]:
        """
        Translate an error.

        Args:
            error: The exception object or error string.
            user_context: What the user was doing (optional).
            tone: "helpful", "professional", "friendly", "witty".

        Returns:
            Dict with keys: title, message, action, severity.
        """
        # Convert exception to string if needed
        raw_message = str(error) if isinstance(error, Exception) else str(error)

        try:
            response = requests.post(
                f"{self.api_url}/translate",
                json={
                    "raw_message": raw_message,
                    "user_context": user_context,
                    "tone": tone,
                },
                timeout=5,
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # Fallback if API is down
            return {
                "title": "Error",
                "message": "An unexpected error occurred and we couldn't get a translation.",
                "action": "Please try again later.",
                "severity": "error",
                "fallback_reason": str(e),
            }


# Sync convenience function
def translate_error(
    error: Exception | str,
    user_context: str = "",
    tone: str = "helpful",
    api_url: str = "http://localhost:8000",
) -> Dict[str, str]:
    """Helper function to translate an error in one line."""
    client = EmpathyClient(api_url)
    return client.translate(error, user_context, tone)
