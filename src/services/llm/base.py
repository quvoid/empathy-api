from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_response(
        self,
        prompt: str,
        system_instruction: str,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a structured JSON response from the LLM.

        Args:
            prompt: User prompt content.
            system_instruction: System instructions/rules.
            config: Generation configuration (temperature, tokens).

        Returns:
            Parsed JSON dictionary.
        """
        pass
