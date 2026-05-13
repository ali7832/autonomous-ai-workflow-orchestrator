from workflow_orchestrator.schemas import Workflow
from workflow_orchestrator.service import WorkflowOrchestrationService


def test_workflow_service_returns_run_metadata():
    workflow = Workflow(
        workflow_id='wf-demo',
        name='Demo workflow',
        submitted_by='operator@example.com',
        environment='staging',
        tasks=[
            {'task_id': 'research', 'name': 'Research', 'agent': 'research', 'payload': {'topic': 'AI monitoring'}},
            {'task_id': 'report', 'name': 'Report', 'agent': 'reporting', 'depends_on': ['research'], 'payload': {'sections': ['summary']}},
        ],
    )

    run = WorkflowOrchestrationService().run(workflow)

    assert run.run_id
    assert run.workflow_id == 'wf-demo'
    assert run.status == 'completed'
    assert run.orchestrator_version
    assert run.total_duration_ms >= 0
    assert [item.task_id for item in run.results] == ['research', 'report']


def test_workflow_service_health_metadata():
    health = WorkflowOrchestrationService().health()

    assert health.status == 'ok'
    assert health.service_name
    assert health.orchestrator_version
