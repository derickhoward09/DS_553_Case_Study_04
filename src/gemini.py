"""Text generation through Google Agent Platform express mode."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


GEMINI_MODELS = ("gemini-3.5-flash-lite", "gemini-3.5-flash")


def generate_review(model, api_key, system_prompt, prompt, max_tokens, timeout):
    if model not in GEMINI_MODELS:
        raise ValueError("Invalid Gemini model")

    endpoint = f"https://aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent"
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens},
    }
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Gemini returned HTTP {error.code}") from None
    except URLError as error:
        if isinstance(error.reason, TimeoutError):
            raise TimeoutError("Gemini request timed out") from None
        raise RuntimeError("Could not reach Gemini Agent Platform") from None
    except ValueError:
        raise RuntimeError("Gemini returned an invalid response") from None

    candidates = result.get("candidates") or [{}]
    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(part.get("text", "") for part in parts if not part.get("thought")).strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response")
    return text
