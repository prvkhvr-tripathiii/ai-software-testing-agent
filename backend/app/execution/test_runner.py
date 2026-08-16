import subprocess


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

    return {
        "command": command,
        "exit_code": result.returncode,
        "passed": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "coverage": coverage_result.stdout,
        "coverage_error": coverage_result.stderr,
    }