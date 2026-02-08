from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import get_settings
from src.models.schemas import TranslateRequest, TranslateResponse
from src.services.translator import get_translator_service

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Translate technical errors into human-friendly messages.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for browser clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.app_name}


@app.post("/translate", response_model=TranslateResponse)
async def translate_error(request: TranslateRequest):
    """
    Translate a technical error into a user-friendly message.

    - **raw_message**: The technical error string (required)
    - **error_code**: Optional application-specific error code
    - **user_context**: What the user was doing when the error occurred
    - **tone**: Desired tone (helpful, professional, friendly, witty)
    """
    try:
        service = get_translator_service()
        return service.translate(request)
    except Exception as e:
        # Even our error handler has a friendly error!
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Translation Failed",
                "message": "We couldn't process your error message right now.",
                "action": "Please try again in a moment.",
                "severity": "error",
            },
        )
