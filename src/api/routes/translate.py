from fastapi import APIRouter, Depends, HTTPException
from src.models.schemas import TranslateRequest, TranslateResponse, Severity
from src.services.translator import get_translator_service, TranslatorService
from src.core.exceptions import EmpathyError

router = APIRouter()


@router.post("/translate", response_model=TranslateResponse)
async def translate_error(
    request: TranslateRequest,
    service: TranslatorService = Depends(get_translator_service),
):
    """
    Translate a technical error into a user-friendly message.
    """
    try:
        return service.translate(request)
    except EmpathyError as e:
        # Domain errors mapped to HTTP status codes
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "title": "Error Processing Request",
                "message": e.message,
                "severity": "error",
                "action": "Please check your request or try again later.",
            },
        )
    except Exception as e:
        # Fallback for unexpected errors
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Internal Server Error",
                "message": "An unexpected error occurred.",
                "severity": "error",
                "action": "Please contact support.",
            },
        )
