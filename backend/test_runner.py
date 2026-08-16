from app.execution.test_runner import run_tests


project = "sample_projects/demo_project"

result = run_tests(project)

print("Exit code:", result["exit_code"])
print("Passed:", result["passed"])

print("\n--- TEST OUTPUT ---")
print(result["stdout"])

print("\n--- TEST ERRORS ---")
print(result["stderr"])

print("\n--- COVERAGE ---")
print(result["coverage"])

print("\n--- COVERAGE ERRORS ---")
print(result["coverage_error"])