from pathlib import Path


def find_python_files(repository_path: str) -> list[str]:
    repository = Path(repository_path)

    if not repository.exists():
        raise FileNotFoundError(
            f"Repository not found: {repository_path}"
        )

    if not repository.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {repository_path}"
        )

    python_files = repository.rglob("*.py")

    return [str(file) for file in python_files]