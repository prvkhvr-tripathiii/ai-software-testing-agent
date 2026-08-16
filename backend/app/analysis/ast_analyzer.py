import ast
from pathlib import Path


def analyze_python_file(file_path: str) -> dict:
    path = Path(file_path)

    source_code = path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "arguments": [
                    argument.arg
                    for argument in node.args.args
                ],
            })

    return {
        "file": str(path),
        "functions": functions,
    }