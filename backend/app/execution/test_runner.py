import subprocess

from app.models.execution import ExecutionResult

from app.execution.result_parser import (
    parse_test_results,
    parse_coverage_results,
)


def run_tests(
    project_path: str,
    test_path: str | None = None,
) -> dict:
    command = [
        "python",
        "-m",
        "coverage",
        "run",
        "-m",
        "pytest",
    ]

    if test_path:
        command.append(test_path)

    result = subprocess.run(
        command,
        cwd=project_path,
        capture_output=True,
        text=True,
    )

    coverage_result = subprocess.run(
        [
            "python",
            "-m",
            "coverage",
            "report",
            "-m",
        ],
        cwd=project_path,
        capture_output=True,
        text=True,
    )

    test_results = parse_test_results(
        result.stdout
    )
    
    coverage_results = parse_coverage_results(
        coverage_result.stdout
    )

    return ExecutionResult(
    command=command,
    exit_code=result.returncode,
    passed=result.returncode == 0,
    tests=test_results,
    coverage=coverage_results,
    stdout=result.stdout,
    stderr=result.stderr,
    coverage_raw=coverage_result.stdout,
    coverage_error=coverage_result.stderr,
)