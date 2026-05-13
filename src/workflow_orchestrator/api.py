from fastapi import FastAPI

from workflow_orchestrator.schemas import HealthResponse, Workflow, WorkflowRun
from workflow_orchestrator.service import WorkflowOrchestrationService

app = FastAPI(title='Autonomous AI Workflow Orchestrator', version='0.2.0')
_service = WorkflowOrchestrationService()


@app.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return _service.health()


@app.post('/workflows/run', response_model=WorkflowRun)
def run_workflow(workflow: Workflow) -> WorkflowRun:
    return _service.run(workflow)
