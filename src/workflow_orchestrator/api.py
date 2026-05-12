from fastapi import FastAPI

from workflow_orchestrator.executor import WorkflowExecutor
from workflow_orchestrator.schemas import Workflow, WorkflowRun

app = FastAPI(title='Autonomous AI Workflow Orchestrator')
_executor = WorkflowExecutor()


@app.get('/health')
def health() -> dict:
    return {'status': 'ok'}


@app.post('/workflows/run', response_model=WorkflowRun)
def run_workflow(workflow: Workflow) -> WorkflowRun:
    return _executor.run(workflow)
