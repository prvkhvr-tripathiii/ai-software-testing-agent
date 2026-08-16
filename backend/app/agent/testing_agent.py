from pathlib import Path

from app.agent.failure_agent import FailureAgent
from app.execution.test_runner import run_tests
from app.analysis.ast_analyzer import analyze_python_file
from app.generation.test_generator import generate_tests
from app.generation.test_writer import write_generated_tests


class TestingAgent:
    """
    Main orchestrator for the AI Software Testing Agent.

    Pipeline:

    Source Code
        ↓
    AST Analysis
        ↓
    Gemini Test Generation
        ↓
    Test File Generation
        ↓
    Test Execution
        ↓
    Results
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.failure_agent = FailureAgent()

    def find_python_files(self) -> list[Path]:
        """
        Find Python source files in the project.

        Test files are excluded because we analyze
        application code first.
        """

        python_files = []

        for file in self.project_path.rglob("*.py"):
            if "tests" in file.parts:
                continue

            python_files.append(file)

        return python_files

    def analyze_file(self, file_path: Path) -> dict:
        """
        Analyze one Python source file using the AST analyzer.
        """

        return analyze_python_file(str(file_path))

    def generate_tests_for_file(
        self,
        file_path: Path,
        analysis: dict,
    ):
        """
        Send source code + analysis to Gemini and generate tests.
        """

        source_code = file_path.read_text(
            encoding="utf-8"
        )

        coverage = {
            "total": 0,
            "files": [],
        }

        return generate_tests(
            source_code=source_code,
            analysis=analysis,
            coverage=coverage,
        )

    def run(self) -> dict:
        """
        Run the complete AI testing pipeline.
        """
    
        python_files = self.find_python_files()
    
        generation_results = []
    
        for file_path in python_files:
            analysis = self.analyze_file(file_path)
    
            generated_tests = self.generate_tests_for_file(
                file_path,
                analysis,
            )
    
            output_file = (
                self.project_path
                / "tests"
                / "generated"
                / f"test_ai_{file_path.stem}.py"
            )
    
            written_file = write_generated_tests(
                tests=generated_tests.tests,
                output_file=str(output_file),
            )
    
            generation_results.append(
                {
                    "source_file": str(
                        file_path.relative_to(self.project_path)
                    ),
                    "generated_test_file": str(
                        Path(written_file).relative_to(
                            self.project_path
                        )
                    ),
                    "tests_generated": len(
                        generated_tests.tests
                    ),
                }
            )
    
        execution_result = run_tests(
            str(self.project_path)
        )
    
        response = {
            "project": str(self.project_path),
            "files_analyzed": len(python_files),
            "generation": generation_results,
            "execution": execution_result.model_dump(),
        }
    
        if not execution_result.passed:
        
            failure_analyses = []
    
            for file_path in python_files:
            
                source_code = file_path.read_text(
                    encoding="utf-8"
                )
    
                failure_analysis = (
                    self.failure_agent.analyze_failure(
                        source_code=source_code,
                        test_output=(
                            execution_result.stdout
                            + "\n"
                            + execution_result.stderr
                        ),
                    )
                )
    
                failure_analyses.append(
                    {
                        "source_file": str(
                            file_path.relative_to(
                                self.project_path
                            )
                        ),
                        "analysis": failure_analysis,
                    }
                )
    
            response["failures"] = failure_analyses
    
        return response