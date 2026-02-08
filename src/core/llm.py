from google import genai
import json
import time
from src.core.config import get_settings


SYSTEM_PROMPT = """You are a UX copywriter specializing in user-facing error messages. Your job is to translate technical error messages into friendly, helpful messages for end-users.

Rules:
1. Never use technical jargon (no "exception", "null", "undefined", "stack trace", etc.)
2. Be empathetic and reassuring - the user didn't do anything wrong.
3. Be concise - max 2 sentences for the message.
4. Always suggest a concrete action the user can take.
5. Match the requested tone (helpful, professional, friendly, witty).

You MUST respond in valid JSON format with this exact structure:
{
  "title": "Short 2-4 word title",
  "message": "1-2 sentence explanation for the user",
  "action": "What the user should do next",
  "severity": "info | warning | error"
}

ONLY output the JSON. No markdown, no explanation, no code blocks."""


class LLMClient:
    """Interface to Google Gemini for error translation."""

    def __init__(self):
        settings = get_settings()
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = "gemini-2.0-flash"

    def translate(
        self,
        raw_message: str,
        user_context: str = "",
        tone: str = "helpful",
        max_retries: int = 3,
    ) -> dict:
        """
        Translate a technical error into a user-friendly message.

        Args:
            raw_message: The sanitized technical error.
            user_context: What the user was doing when the error occurred.
            tone: The desired tone (helpful, professional, friendly, witty).
            max_retries: Number of retries for rate limit errors.

        Returns:
            A dictionary with title, message, action, and severity.
        """
        full_prompt = f"""{SYSTEM_PROMPT}

Translate this error for an end-user.

Error: {raw_message}
User was doing: {user_context or "Unknown action"}
Desired tone: {tone}"""

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt,
                )

                # Clean response text (remove potential markdown code blocks)
                text = response.text.strip()
                if text.startswith("```"):
                    lines = text.split("\n")
                    text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
                    text = text.rstrip("`").strip()

                return json.loads(text)

            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    # Rate limited - wait and retry
                    wait_time = (attempt + 1) * 5  # 5s, 10s, 15s
                    time.sleep(wait_time)
                    continue
                raise

        # If all retries failed, return a fallback response
        return {
            "title": "Something Went Wrong",
            "message": "We're experiencing high demand right now.",
            "action": "Please try again in a few moments.",
            "severity": "warning",
        }
