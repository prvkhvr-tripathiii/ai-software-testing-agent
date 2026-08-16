import json

from app.agent.testing_agent import TestingAgent


PROJECT_PATH = "sample_projects/demo_project"


agent = TestingAgent(PROJECT_PATH)

result = agent.run()

print(json.dumps(result, indent=2))
