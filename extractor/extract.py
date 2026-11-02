import json
from pathlib import Path

from pydantic import ValidationError

from extractor.schema import CVData
from llm_client.client import LLMClient


def extract_cv(cv_text: str) -> CVData:
    prompt = Path("prompts/cv_extraction_v1.txt").read_text()
    repair_prompt = Path("prompts/cv_repair_v1.txt").read_text()

    client = LLMClient()

    try:
        response = client.chat(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": cv_text},
            ]
        )

        result = response["choices"][0]["message"]["content"]

        for attempt in range(2):
            try:
                result = result.strip()

                if result.startswith("```"):
                    result = result.split("\n", 1)[1]
                    result = result.rsplit("```", 1)[0].strip()

                data = json.loads(result)
                return CVData.model_validate(data)

            except (json.JSONDecodeError, ValidationError) as exc:
                if attempt == 1:
                    raise

                repair_response = client.chat(
                    messages=[
                        {
                            "role": "system",
                            "content": repair_prompt,
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Original CV:\n{cv_text}\n\n"
                                f"Invalid response:\n{result}\n\n"
                                f"Validation error:\n{exc}"
                            ),
                        },
                    ]
                )

                result = repair_response["choices"][0]["message"]["content"]

        raise RuntimeError("CV extraction failed after repair attempt")

    finally:
        client.close()
