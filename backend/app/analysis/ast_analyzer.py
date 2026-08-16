import ast
from pathlib import Path


def analyze_python_file(file_path: str) -> dict:
    path = Path(file_path)

    source_code = path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)

    functions = []
    classes = []

    for node in ast.iter_child_nodes(tree):

        # Top-level functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(analyze_function(node))

        # Classes
        elif isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "line": node.lineno,
                "methods": []
            }

            for child in node.body:
                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    class_info["methods"].append(
                        analyze_function(child)
                    )

            classes.append(class_info)

    return {
        "file": str(path),
        "functions": functions,
        "classes": classes,
    }


def analyze_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict:
    function_info = {
        "name": node.name,
        "line": node.lineno,
        "arguments": [
            argument.arg
            for argument in node.args.args
        ],
        "branches": [],
        "loops": [],
        "exceptions": [],
        "try_blocks": [],
    }

    for child in ast.walk(node):

        # if / elif
        if isinstance(child, ast.If):
            function_info["branches"].append({
                "condition": ast.unparse(child.test),
                "line": child.lineno,
            })

        # for / while
        elif isinstance(child, (ast.For, ast.While)):
            function_info["loops"].append({
                "type": "for" if isinstance(child, ast.For) else "while",
                "line": child.lineno,
            })

        # raise
        elif isinstance(child, ast.Raise):
            exception_type = "Unknown"

            if isinstance(child.exc, ast.Call):
                if isinstance(child.exc.func, ast.Name):
                    exception_type = child.exc.func.id

            elif isinstance(child.exc, ast.Name):
                exception_type = child.exc.id

            function_info["exceptions"].append({
                "type": exception_type,
                "line": child.lineno,
            })

        # try / except
        elif isinstance(child, ast.Try):
            handlers = []

            for handler in child.handlers:
                if handler.type is not None:
                    handlers.append(
                        ast.unparse(handler.type)
                    )
                else:
                    handlers.append("Exception")

            function_info["try_blocks"].append({
                "line": child.lineno,
                "handlers": handlers,
            })

    return function_info