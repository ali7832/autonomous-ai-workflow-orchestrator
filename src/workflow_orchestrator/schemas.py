from __future__ import annotations

from pydantic import BaseModel, Field


class Task(BaseModel):
    task_id: str
    name: str
    agent: str = 'general'
    depends_on: list[str] = []
    payload: dict = {}
    timeout_seconds: int | None = None
    critical: bool = True


class Workflow(BaseModel):
    workflow_id: str
    name: str
    tasks: list[Task] = Field(..., min_length=1)
    submitted_by: str | None = None
    environment: str = 'local'


class TaskResult(BaseModel):
    task_id: str
    status: str
    agent: str
    output: dict
    duration_ms: float
    dependencies: list[str]


class WorkflowRun(BaseModel):
    run_id: str
    workflow_id: str
    status: str
    orchestrator_version: str
    environment: str
    total_duration_ms: float
    results: list[TaskResult]


class HealthResponse(BaseModel):
    status: str
    service_name: str
    environment: str
    orchestrator_version: str
