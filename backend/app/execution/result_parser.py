import re
from app.models.execution import (
    TestResult,
    FileCoverage,
    CoverageResult,
)


def parse_test_results(stdout: str) -> dict:
    passed = 0
    failed = 0
    errors = 0

    passed_match = re.search(r"(\d+) passed", stdout)
    failed_match = re.search(r"(\d+) failed", stdout)
    error_match = re.search(r"(\d+) error", stdout)

    if passed_match:
        passed = int(passed_match.group(1))

    if failed_match:
        failed = int(failed_match.group(1))

    if error_match:
        errors = int(error_match.group(1))

    return TestResult(
        passed=passed,
        failed=failed,
        errors=errors,
        total=passed + failed + errors,
    )


def parse_coverage_results(stdout: str) -> dict:
    files = []
    total_coverage = 0

    lines = stdout.splitlines()

    for line in lines:
        line = line.strip()

        if not line or line.startswith("-"):
            continue

        parts = line.split()

        if len(parts) < 4:
            continue

        filename = parts[0]

        if filename == "Name":
            continue

        if filename == "TOTAL":
            try:
                total_coverage = int(
                    parts[3].replace("%", "")
                )
            except ValueError:
                pass

            continue

        try:
            statements = int(parts[1])
            missing = int(parts[2])
            coverage = int(parts[3].replace("%", ""))
        except ValueError:
            continue

        missing_lines = []

        if len(parts) >= 5:
            missing_text = " ".join(parts[4:])

            for value in missing_text.split(","):
                value = value.strip()

                if value.isdigit():
                    missing_lines.append(int(value))

        files.append(
            FileCoverage(
                file=filename,
                statements=statements,
                missing=missing,
                coverage=coverage,
                missing_lines=missing_lines,
            )
        )

    return CoverageResult(
        total=total_coverage,
        files=files,
    )
