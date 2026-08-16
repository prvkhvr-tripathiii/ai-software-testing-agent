from pydantic import BaseModel, Field


class TestResult(BaseModel):
    total: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0


class FileCoverage(BaseModel):
    file: str
    statements: int
    missing: int
    coverage: float
    missing_lines: list[int] = Field(default_factory=list)


class CoverageResult(BaseModel):
    total: float = 0
    files: list[FileCoverage] = Field(default_factory=list)


class ExecutionResult(BaseModel):
    command: list[str]
    exit_code: int
    passed: bool

    tests: TestResult
    coverage: CoverageResult

    stdout: str = ""
    stderr: str = ""
    coverage_raw: str = ""
    coverage_error: str = ""