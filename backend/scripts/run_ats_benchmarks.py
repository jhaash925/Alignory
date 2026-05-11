import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "benchmarks" / "ats_cases.json"
sys.path.insert(0, str(ROOT))

from app.services.ats_engine import build_ats_breakdown


def load_cases():
    with CASES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_case(case):
    breakdown = build_ats_breakdown(
        case["job_description"],
        case["resume_text"],
        case["parsed_resume"],
    )

    score = breakdown["overall_score"]
    matched_names = {item["name"] for item in breakdown["matched_requirements"]}
    missing_names = {item["name"] for item in breakdown["missing_requirements"]}
    low, high = case["expected"]["score_range"]

    errors = []

    if not (low <= score <= high):
        errors.append(f"score {score} not in expected range [{low}, {high}]")

    for name in case["expected"].get("matched_requirements", []):
        if name not in matched_names:
            errors.append(f"expected matched requirement missing: {name}")

    for name in case["expected"].get("missing_requirements", []):
        if name not in missing_names:
            errors.append(f"expected missing requirement not missing: {name}")

    return {
        "id": case["id"],
        "description": case["description"],
        "score": score,
        "errors": errors,
        "matched_preview": sorted(list(matched_names))[:6],
        "missing_preview": sorted(list(missing_names))[:6],
    }


def main():
    cases = load_cases()
    results = [evaluate_case(case) for case in cases]
    failures = [result for result in results if result["errors"]]

    for result in results:
        status = "PASS" if not result["errors"] else "FAIL"
        print(f"[{status}] {result['id']}: score={result['score']}")
        print(f"  {result['description']}")
        print(f"  matched: {', '.join(result['matched_preview']) or 'none'}")
        print(f"  missing: {', '.join(result['missing_preview']) or 'none'}")

        for error in result["errors"]:
            print(f"  - {error}")

    print()
    print(f"Cases: {len(results)}")
    print(f"Failures: {len(failures)}")

    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
