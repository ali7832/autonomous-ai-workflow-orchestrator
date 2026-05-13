from __future__ import annotations

import time
from uuid import uuid4

from workflow_orchestrator.agents import get_agent
from workflow_orchestrator.config import settings
from workflow_orchestrator.schemas import TaskResult, Workflow, WorkflowRun


class WorkflowExecutor:
    def run(self, workflow: Workflow) -> WorkflowRun:
        started = time.perf_counter()
        run_id = str(uuid4())
        completed: set[str] = set()
        results: list[TaskResult] = []
        remaining = list(workflow.tasks)

        if len(remaining) > settings.max_tasks_per_workflow:
            raise ValueError('workflow exceeds maximum configured task count')

        while remaining:
            progressed = False
            for task in list(remaining):
                if all(dep in completed for dep in task.depends_on):
                    task_started = time.perf_counter()
                    agent = get_agent(task.agent)
                    output = agent.run(task.payload)
                    duration_ms = round((time.perf_counter() - task_started) * 1000, 2)
                    results.append(
                        TaskResult(
                            task_id=task.task_id,
                            status='completed',
                            agent=agent.name,
                            output=output,
                            duration_ms=duration_ms,
                            dependencies=task.depends_on,
                        )
                    )
                    completed.add(task.task_id)
                    remaining.remove(task)
                    progressed = True
            if not progressed:
                raise ValueError('workflow contains unresolved dependencies or a cycle')

        total_duration_ms = round((time.perf_counter() - started) * 1000, 2)
        return WorkflowRun(
            run_id=run_id,
            workflow_id=workflow.workflow_id,
            status='completed',
            orchestrator_version=settings.orchestrator_version,
            environment=workflow.environment,
            total_duration_ms=total_duration_ms,
            results=results,
        )
