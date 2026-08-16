from app.agent.failure_agent import FailureAgent


source = """
def divide(a,b):
    return a/b
"""


failure = """
FAILED test_divide_zero

ZeroDivisionError:
division by zero
"""


agent = FailureAgent()

result = agent.analyze_failure(
    source,
    failure
)

print(result)