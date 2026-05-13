from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class WorkflowSettings:
    environment: str = os.getenv('WORKFLOW_ENV', 'local')
    service_name: str = os.getenv('WORKFLOW_SERVICE_NAME', 'autonomous-ai-workflow-orchestrator')
    orchestrator_version: str = os.getenv('WORKFLOW_ORCHESTRATOR_VERSION', 'dag-executor-v1')
    run_store_path: str = os.getenv('WORKFLOW_RUN_STORE_PATH', 'workflow_runs.jsonl')
    default_task_timeout_seconds: int = int(os.getenv('WORKFLOW_DEFAULT_TASK_TIMEOUT_SECONDS', '60'))
    max_tasks_per_workflow: int = int(os.getenv('WORKFLOW_MAX_TASKS_PER_WORKFLOW', '50'))


settings = WorkflowSettings()
