import os
import subprocess
from pathlib import Path

from app.execution.result_parser import parse_test_results


def run_tests(
    project_path: str,
    test_path: str = "tests/generated",
) -> dict:
    """
    Run pytest with coverage inside the target project.
    """

    project_root = Path(project_path).resolve()

    command = [
        "python",
        "-m",
        "coverage",
        "run",
        "-m",
        "pytest",
	test_path,
    ]

    environment = os.environ.copy()

    # Make the target project's root importable.
    existing_pythonpath = environment.get("PYTHONPATH", "")

    if existing_pythonpath:
        environment["PYTHONPATH"] = (
            str(project_root)
            + os.pathsep
            + existing_pythonpath
        )
    else:
        environment["PYTHONPATH"] = str(project_root)

    result = subprocess.run(
        command,
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
    )

    coverage_result = subprocess.run(
        [
            "python",
            "-m",
            "coverage",
            "report",
        ],
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
    )

    parsed = parse_test_results(result.stdout)

    return parsed
