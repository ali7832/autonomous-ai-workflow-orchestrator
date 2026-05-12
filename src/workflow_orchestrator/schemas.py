from __future__ import annotations

from pydantic import BaseModel


class Task(BaseModel):
    task_id: str
    name: str
    agent: str = 'general'
    depends_on: list[str] = []
    payload: dict = {}


class Workflow(BaseModel):
    workflow_id: str
    name: str
    tasks: list[Task]


class TaskResult(BaseModel):
    task_id: str
    status: str
    agent: str
    output: dict


class WorkflowRun(BaseModel):
    workflow_id: str
    status: str
    results: list[TaskResult]
