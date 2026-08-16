import os

from google import genai
from google.genai import types
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

    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set."
        )

    client = genai.Client()

    prompt = f"""
You are an expert Python software testing engineer.

Your task is to generate high-quality pytest tests for the provided
Python source code.

Your primary goal is to improve test coverage.

Prioritize:
1. Uncovered lines.
2. Uncovered branches.
3. Exception paths.
4. Edge cases.
5. Boundary conditions.
6. Important normal behavior.

Do not generate unnecessary duplicate tests.

SOURCE CODE:
{source_code}

AST ANALYSIS:
{analysis}

CURRENT COVERAGE:
{coverage}

Generate pytest tests for the source code.

Requirements:
- Use pytest.
- Generated tests must be valid Python.
- Import the functions/classes being tested.
- Test actual behavior, not implementation details.
- If a branch raises an exception, test that exception.
- Focus especially on currently uncovered code.
- Do not include markdown fences.
- Return only the structured response.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TestGenerationResponse,
            ),
        )

        if not response.parsed:
            raise RuntimeError(
                "Gemini returned an empty or invalid structured response."
            )

        return response.parsed

    except Exception as error:
        raise RuntimeError(
            f"Gemini test generation failed: {error}"
        ) from error
