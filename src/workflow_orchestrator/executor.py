from __future__ import annotations

from workflow_orchestrator.agents import get_agent
from workflow_orchestrator.schemas import TaskResult, Workflow, WorkflowRun


class WorkflowExecutor:
    def run(self, workflow: Workflow) -> WorkflowRun:
        completed: set[str] = set()
        results: list[TaskResult] = []
        remaining = list(workflow.tasks)

        while remaining:
            progressed = False
            for task in list(remaining):
                if all(dep in completed for dep in task.depends_on):
                    agent = get_agent(task.agent)
                    output = agent.run(task.payload)
                    results.append(
                        TaskResult(
                            task_id=task.task_id,
                            status='completed',
                            agent=agent.name,
                            output=output,
                        )
                    )
                    completed.add(task.task_id)
                    remaining.remove(task)
                    progressed = True
            if not progressed:
                raise ValueError('workflow contains unresolved dependencies or a cycle')

        return WorkflowRun(workflow_id=workflow.workflow_id, status='completed', results=results)
