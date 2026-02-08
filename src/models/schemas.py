from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class Tone(str, Enum):
    """Available tones for the translated message."""

    HELPFUL = "helpful"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    WITTY = "witty"


class Severity(str, Enum):
    """Severity level of the error."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class TranslateRequest(BaseModel):
    """Request schema for the /translate endpoint."""

    raw_message: str = Field(
        ...,
        description="The raw technical error message or exception string.",
        min_length=1,
        max_length=2000,
        examples=["ZeroDivisionError: division by zero"],
    )
    error_code: Optional[str] = Field(
        None,
        description="Optional error code (e.g., 'E001', 'AUTH_FAILED').",
        max_length=50,
        examples=["E001"],
    )
    user_context: Optional[str] = Field(
        None,
        description="What the user was doing when the error occurred.",
        max_length=500,
        examples=["User was trying to save their profile picture"],
    )
    tone: Tone = Field(
        Tone.HELPFUL,
        description="The desired tone for the translated message.",
    )


class TranslateResponse(BaseModel):
    """Response schema for the /translate endpoint."""

    title: str = Field(..., description="Short 2-4 word title for the error.")
    message: str = Field(..., description="User-friendly explanation of the error.")
    action: str = Field(..., description="Suggested action for the user to take.")
    severity: Severity = Field(..., description="Severity level of the error.")
    cached: bool = Field(False, description="Whether this response was served from cache.")
