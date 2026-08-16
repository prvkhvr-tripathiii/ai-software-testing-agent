from app.analysis.ast_analyzer import analyze_python_file
from app.generation.test_generator import generate_tests
from app.generation.test_writer import write_generated_tests


source_file = "sample_projects/demo_project/calculator.py"


with open(source_file, "r", encoding="utf-8") as file:
    source_code = file.read()


analysis = analyze_python_file(source_file)


coverage = {
    "total": 90,
    "files": [
        {
            "file": "calculator.py",
            "statements": 10,
            "missing": 2,
            "coverage": 80,
            "missing_lines": [13, 17],
        }
    ],
}


result = generate_tests(
    source_code=source_code,
    analysis=analysis,
    coverage=coverage,
)


output_file = "sample_projects/demo_project/tests/test_ai_generated.py"

written_file = write_generated_tests(
    tests=result.tests,
    output_file=output_file,
)

print(f"Generated tests written to: {written_file}")


print(result.model_dump_json(indent=2))
