# CV Extractor and Multimodal Invoice Extraction

## Project Overview

This project demonstrates how to build an OpenAI-compatible LLM client, extract structured information from CVs, compare hosted and local models, and extract invoice details from images and scanned PDFs.

All sample people, companies, addresses and numbers are invented.

## Technologies Used

- Python
- OpenAI-compatible API
- Ollama
- Groq
- Qwen 2.5 0.5B
- Qwen 3.5 2B
- Pydantic
- HTTPX
- PyMuPDF
- Pytest
- Ruff

## Project Structure

```text
cvextractor/
├── llm_client/       # LLM client and settings
├── extractor/        # CV and invoice schemas and extraction
├── prompts/          # Versioned extraction prompts
├── data/
│   ├── cvs/          # 20 synthetic CVs
│   ├── invoice_image/
│   └── scanned_image/
├── results/
│   ├── extracted_cvs/
│   ├── hosted/
│   ├── accuracy.csv
│   ├── hosted_results.csv
│   ├── model_comparison.csv
│   └── experiments.md
├── tests/            # Unit tests
├── main.py
├── test_invoice_vision.py
├── pyproject.toml
└── README.md
```

## Setup

Install dependencies:

```bash
uv sync
```

Create a `.env` file using `.env.example` and configure the LLM settings.

Never commit API keys or secrets.

## Run CV Extraction

```bash
uv run python main.py
```

## Run Invoice Vision Extraction

Make sure Ollama is running and the vision model is available:

```bash
ollama pull qwen3.5:2b
```

Run:

```bash
uv run python test_invoice_vision.py
```

## Run Tests and Quality Checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Experiments and Results

- Compared local and hosted LLM models using 10 CVs.
- Manually checked extracted CV fields.
- Tested temperature 0 and temperature 1.
- Tested fixed seed generation.
- Experimented with a limited context size.
- Extracted invoice fields from an invoice image and a scanned PDF.
- Validated structured invoice responses using Pydantic.

See `results/experiments.md` and the CSV files in `results/` for details.

## Security Considerations

- Treat CVs and invoices as untrusted input.
- Keep document content separate from system instructions.
- Do not expose API keys or secrets.
- Validate model responses using Pydantic.
- Do not assume extracted values are factually correct without verification.
