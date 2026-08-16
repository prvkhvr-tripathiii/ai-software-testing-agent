from google import genai


class FailureAgent:
    """
    Analyzes failed test executions using Gemini.
    """

    def __init__(self):
        self.client = genai.Client()

    def analyze_failure(
        self,
        source_code: str,
        test_output: str,
    ) -> dict:

        prompt = f"""
You are an expert Python debugging assistant.

Analyze this failed test execution.

SOURCE CODE:
{source_code}


TEST FAILURE OUTPUT:
{test_output}


Return JSON:

{{
    "issue": "",
    "root_cause": "",
    "suggested_fix": "",
    "severity": "low|medium|high"
}}
"""

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return {
            "analysis": response.text
        }
