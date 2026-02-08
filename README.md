# Empathy API (with Google Gemini)

**Stop showing users "Error 500". Start showing them solutions.**

The Empathy API is a middleware service that uses **Google's Gemini LLM** to translate raw, technical error logs into clear, actionable, and human-friendly messages for your end-users.

Instead of writing thousands of `if (error.code === '...'):` checks, you just send the error to this API, and it returns a perfect, context-aware message.

## Key Features

- **Standardized Response:** Always returns `title`, `message`, `action`, and `severity`.
- **Smart Translation:** Understands context (e.g., `ZeroDivisionError` -> "Calculation issue").
- **Privacy First:** automatically strips **emails, IP addresses, API keys, and JWT tokens** before sending data to Gemini.
- **Cost Efficient:** caches responses for 24 hours so you don't pay for the same error twice.
- **Fail-Safe:** Includes retry logic for rate limits and a fallback message if the LLM is down.

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your Gemini API Key
echo "GEMINI_API_KEY=your_key_here" > .env
```
*Get a free API key here: [Google AI Studio](https://aistudio.google.com/app/apikey)*

### 2. Run Server

```bash
python -m uvicorn src.main:app --reload
```
Runs on `http://localhost:8000`.

## Usage Example

Send a `POST` request to `/translate` with your raw technical error:

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "raw_message": "ConnectionRefusedError: [WinError 10061] No connection could be made",
    "user_context": "User was trying to sync their offline data",
    "tone": "helpful"
  }'
```

### Response

```json
{
  "title": "Sync Failed",
  "message": "We couldn't connect to the server to sync your data.",
  "action": "Please check your internet connection and try again.",
  "severity": "warning",
  "cached": false
}
```

## API Reference

**POST /translate**

| Field | Type | Description |
|-------|------|-------------|
| `raw_message` | string | **Required**. The technical error (e.g., stack trace). |
| `user_context`| string | Optional. What the user was doing (e.g., "Uploading file"). |
| `tone` | string | Optional. `helpful`, `professional`, `friendly`, `witty`. |
