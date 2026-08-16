from pprint import pprint

from app.execution.test_runner import run_tests


project = "sample_projects/demo_project"

result = run_tests(project)

pprint(result)