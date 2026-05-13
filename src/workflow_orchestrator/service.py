from __future__ import annotations

from workflow_orchestrator.config import settings
from workflow_orchestrator.executor import WorkflowExecutor
from workflow_orchestrator.schemas import HealthResponse, Workflow, WorkflowRun
from workflow_orchestrator.storage import append_workflow_run


class WorkflowOrchestrationService:
    def __init__(self) -> None:
        self.executor = WorkflowExecutor()

    def health(self) -> HealthResponse:
        return HealthResponse(
            status='ok',
            service_name=settings.service_name,
            environment=settings.environment,
            orchestrator_version=settings.orchestrator_version,
        )

    def run(self, workflow: Workflow) -> WorkflowRun:
        run = self.executor.run(workflow)
        append_workflow_run(
            {
                'run_id': run.run_id,
                'workflow_id': workflow.workflow_id,
                'submitted_by': workflow.submitted_by,
                'environment': workflow.environment,
                'status': run.status,
                'task_count': len(workflow.tasks),
                'total_duration_ms': run.total_duration_ms,
                'run': run.model_dump(),
            },
            settings.run_store_path,
        )
        return run
