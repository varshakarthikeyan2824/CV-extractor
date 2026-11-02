import random
import time
from typing import Any

import httpx

from llm_client.settings import settings


class LLMClient:
    """Client for calling OpenAI-compatible LLM APIs."""

    def __init__(
        self,
        models: list[str] | None = None,
    ) -> None:
        self.models = models or [settings.model]
        self.client = httpx.Client(
            base_url=settings.base_url,
            headers={"Authorization": f"Bearer {settings.api_key}"},
            timeout=settings.timeout,
        )

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.0,
        seed: int | None = None,
    ) -> dict[str, Any]:
        last_error: Exception | None = None

        for model in self.models:
            for attempt in range(settings.max_retries + 1):
                try:
                    response = self.client.post(
                        "chat/completions",
                        json={
                            "model": model,
                            "messages": messages,
                            "temperature": temperature,
                            "seed": seed,
                        },
                    )

                    if response.status_code == 429 or response.status_code >= 500:
                        if attempt == settings.max_retries:
                            response.raise_for_status()

                        retry_after = response.headers.get("Retry-After")
                        delay = (
                            float(retry_after)
                            if retry_after
                            else min(2**attempt, 30) + random.uniform(0, 1)
                        )
                        time.sleep(delay)
                        continue

                    response.raise_for_status()
                    return response.json()

                except (httpx.TimeoutException, httpx.TransportError) as exc:
                    last_error = exc

                    if attempt == settings.max_retries:
                        break

                    delay = min(2**attempt, 30) + random.uniform(0, 1)
                    time.sleep(delay)

                except httpx.HTTPStatusError as exc:
                    last_error = exc
                    break

        raise RuntimeError("All configured LLM models failed") from last_error

    def close(self) -> None:
        self.client.close()
