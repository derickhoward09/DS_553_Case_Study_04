import io
import json
from unittest.mock import Mock
from urllib.error import HTTPError

import pytest

import app
from src import gemini


@pytest.fixture
def gemini_api(monkeypatch):
    monkeypatch.setattr(app, "PRODUCT_MODE", "api")
    monkeypatch.setattr(app, "API_PROVIDER", "gemini")


def review(model):
    return app.analyze_resume(
        "Sam Example, analyst", "General Resume Review", "", 512, 0.3, False, model
    )


@pytest.mark.parametrize("model", gemini.GEMINI_MODELS)
def test_selected_model_uses_agent_platform(gemini_api, monkeypatch, model):
    monkeypatch.setenv("GOOGLE_AGENT_PLATFORM_API_KEY", "test-key")
    body = {
        "candidates": [
            {"content": {"parts": [{"text": "thought", "thought": True}, {"text": "feedback"}]}}
        ]
    }
    send = Mock(return_value=io.BytesIO(json.dumps(body).encode()))
    monkeypatch.setattr(gemini, "urlopen", send)

    feedback, information = review(model)

    assert feedback == "feedback"
    assert model in information
    request = send.call_args.args[0]
    assert request.full_url == (
        f"https://aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent"
    )
    assert request.get_header("X-goog-api-key") == "test-key"
    payload = json.loads(request.data)
    assert payload["systemInstruction"]["parts"][0]["text"] == app.SYSTEM_PROMPT
    assert "Sam Example" in payload["contents"][0]["parts"][0]["text"]
    assert payload["generationConfig"] == {"maxOutputTokens": 512}


def test_missing_key_stops_inference(gemini_api, monkeypatch):
    monkeypatch.delenv("GOOGLE_AGENT_PLATFORM_API_KEY", raising=False)
    send = Mock()
    monkeypatch.setattr(gemini, "urlopen", send)

    with pytest.raises(app.gr.Error, match="GOOGLE_AGENT_PLATFORM_API_KEY is missing"):
        review(gemini.GEMINI_MODELS[0])

    send.assert_not_called()


def test_provider_error_does_not_expose_key(gemini_api, monkeypatch):
    monkeypatch.setenv("GOOGLE_AGENT_PLATFORM_API_KEY", "test-key")
    error = HTTPError("https://example.invalid", 403, "test-key", None, None)
    monkeypatch.setattr(gemini, "urlopen", Mock(side_effect=error))

    with pytest.raises(app.gr.Error, match="Gemini returned HTTP 403") as raised:
        review(gemini.GEMINI_MODELS[0])

    assert "test-key" not in str(raised.value)
