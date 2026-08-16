from pathlib import Path

from app.generation.test_generator import GeneratedTest


def write_generated_tests(
    tests: list[GeneratedTest],
    output_file: str,
) -> str:
    """
    Write AI-generated pytest tests to a Python file.

    Each GeneratedTest contains the complete test function/code.
    """

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    test_blocks = []

    for test in tests:
        test_blocks.append(
            f"# Generated test: {test.name}\n"
            f"# Target function: {test.target_function}\n\n"
            f"{test.code.strip()}"
        )

    content = "\n\n\n".join(test_blocks)

    output_path.write_text(
        content + "\n",
        encoding="utf-8",
    )

    return str(output_path)
