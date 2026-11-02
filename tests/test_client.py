import httpx

from llm_client.client import LLMClient


def test_chat_returns_response():
    """Check that the client returns a successful API response."""

    def fake_response(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "Hello from the test model"}}],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
            },
        )

    transport = httpx.MockTransport(fake_response)

    client = LLMClient(models=["test-model"])
    client.client.close()
    client.client = httpx.Client(
        base_url="http://test",
        transport=transport,
    )

    result = client.chat(messages=[{"role": "user", "content": "Hello"}])

    assert result["choices"][0]["message"]["content"] == ("Hello from the test model")
    assert result["usage"]["total_tokens"] == 15

    client.close()


def test_chat_retries_after_server_error():
    """Check that the client retries after a 500 server error."""

    attempts = 0

    def fake_response(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        if attempts == 1:
            return httpx.Response(500, json={"error": "Server error"})

        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "Success after retry"}}],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
            },
        )

    transport = httpx.MockTransport(fake_response)

    client = LLMClient(models=["test-model"])
    client.client.close()
    client.client = httpx.Client(
        base_url="http://test",
        transport=transport,
    )

    result = client.chat(messages=[{"role": "user", "content": "Hello"}])

    assert attempts == 2
    assert result["choices"][0]["message"]["content"] == ("Success after retry")

    client.close()


def test_chat_handles_timeout(monkeypatch):
    """Check that the client handles a timeout."""

    def fake_response(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Request timed out")

    monkeypatch.setattr("llm_client.client.settings.max_retries", 0)

    client = LLMClient(models=["test-model"])
    client.client.close()
    client.client = httpx.Client(
        base_url="http://test",
        transport=httpx.MockTransport(fake_response),
    )

    try:
        try:
            client.chat(messages=[{"role": "user", "content": "Hello"}])
            assert False, "Expected timeout failure"
        except RuntimeError as exc:
            assert "models failed" in str(exc)
    finally:
        client.close()


def test_chat_uses_fallback_model():
    """Check that the client tries another model if the first fails."""

    attempted_models = []

    def fake_response(request: httpx.Request) -> httpx.Response:
        model = request.read()
        import json

        model_name = json.loads(model)["model"]
        attempted_models.append(model_name)

        if model_name == "first-model":
            return httpx.Response(
                404,
                json={"error": "Model not found"},
            )

        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "Fallback success"}}],
                "usage": {"total_tokens": 10},
            },
        )

    client = LLMClient(models=["first-model", "second-model"])
    client.client.close()
    client.client = httpx.Client(
        base_url="http://test",
        transport=httpx.MockTransport(fake_response),
    )

    try:
        result = client.chat(messages=[{"role": "user", "content": "Hello"}])

        assert attempted_models == ["first-model", "second-model"]
        assert result["choices"][0]["message"]["content"] == ("Fallback success")
    finally:
        client.close()
