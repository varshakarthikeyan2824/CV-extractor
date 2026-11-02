import csv
import time
from pathlib import Path

from extractor.extract import extract_cv

cv_folder = Path("data/cvs")
output_folder = Path("results/hosted")
output_folder.mkdir(parents=True, exist_ok=True)

results = []

for cv_file in sorted(cv_folder.glob("*.txt"))[:10]:
    start = time.perf_counter()

    try:
        cv_text = cv_file.read_text()
        extracted = extract_cv(cv_text)

        output_file = output_folder / f"{cv_file.stem}.json"
        output_file.write_text(extracted.model_dump_json(indent=2))

        status = "Success"

    except (ValueError, KeyError, RuntimeError, OSError) as error:
        status = "Failed"
        print(f"{cv_file.name}: {error}")

    elapsed = round(time.perf_counter() - start, 2)

    results.append(
        {
            "CV": cv_file.stem,
            "Time_seconds": elapsed,
            "Status": status,
        }
    )

    print(f"{cv_file.name}: {status}, {elapsed} seconds")

with open("results/hosted_results.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["CV", "Time_seconds", "Status"],
    )
    writer.writeheader()
    writer.writerows(results)

print("\nHosted model processing completed!")
