
# Local Model Experiments

## Model Details
- Model: qwen2.5:0.5b
- Platform: Ollama
- Purpose: Compare output consistency under different settings.

## Experiment 1: Temperature 0
Status: Completed

- Temperature: 0
- Number of runs: 3
- Result: All three outputs were exactly identical.
- Observation: The model produced consistent extraction results.

## Experiment 2: High Temperature
Status: Completed

- Temperature: 1.0
- Number of runs: 3
- Result: All three outputs were identical.
- Observation: No changes in field values, skills, experience, education, or JSON structure compared with temperature 0.

## Experiment 3: Fixed Seed
Status: Completed

- Temperature: 0
- Fixed seed: 42
- CV: cv_01
- Result: Successfully generated valid JSON.
- Observation: The extracted fields matched the original CV.

## Experiment 4: Context Size (num_ctx)
Status: In progress

- Original model: qwen2.5:0.5b
- Experimental model: qwen-small-context
- Explicit num_ctx: 2048
- Normal CV test: Pending
- Long document test: Pending

## Experiment 5: Multimodal Invoice Extraction

Status: Completed

- Vision model: qwen3.5:2b
- Platform: Ollama
- Input 1: Invoice PNG image
- Input 2: Scanned PDF converted to PNG
- Extraction: Invoice number, date, vendor, customer, subtotal, tax and total
- JSON parsing: Successful for both inputs
- Pydantic validation: Successful for both inputs
- Observation: The model extracted invoice fields from both image formats.
- Limitation: Vendor and customer names were marked as invented in some outputs and require manual verification.
