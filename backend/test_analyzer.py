from app.analysis.repository import find_python_files
from app.analysis.ast_analyzer import analyze_python_file


repository = "sample_projects/demo_project"

files = find_python_files(repository)

for file in files:
    analysis = analyze_python_file(file)

    print(f"\nFile: {analysis['file']}")

    for function in analysis["functions"]:
        print(f"  Function: {function['name']}")
        print(f"  Line: {function['line']}")
        print(f"  Arguments: {function['arguments']}")