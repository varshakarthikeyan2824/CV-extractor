from pathlib import Path

from extractor.extract import extract_cv

cv_folder = Path("data/cvs")
output_folder = Path("results/extracted_cvs")

output_folder.mkdir(parents=True, exist_ok=True)

for cv_file in sorted(cv_folder.glob("*.txt")):
    print(f"Processing: {cv_file.name}")

    cv_text = cv_file.read_text()
    result = extract_cv(cv_text)

    output_file = output_folder / f"{cv_file.stem}.json"
    output_file.write_text(result.model_dump_json(indent=2))

    print(f"Saved: {output_file.name}")

print("All CVs processed!")
