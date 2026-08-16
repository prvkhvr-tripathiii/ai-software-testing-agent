from pydantic import BaseModel, Field


class GeneratedTest(BaseModel):
    name: str
    code: str
    target_function: str


class TestGenerationRequest(BaseModel):
    source_code: str
    analysis: dict
    coverage: dict


class TestGenerationResponse(BaseModel):
    tests: list[GeneratedTest] = Field(default_factory=list)


def generate_tests(
    source_code: str,
    analysis: dict,
    coverage: dict,
) -> TestGenerationResponse:

    tests = []

    for function in analysis.get("functions", []):
        test_name = f"test_{function['name']}"

        test_code = f"""
        
def {test_name}():
    # TODO: AI-generated test
    pass
""".strip()

        tests.append(
            GeneratedTest(
                name=test_name,
                code=test_code,
                target_function=function["name"],
            )
        )

    return TestGenerationResponse(tests=tests)