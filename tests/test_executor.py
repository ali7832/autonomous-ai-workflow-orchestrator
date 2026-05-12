import pytest

from workflow_orchestrator.executor import WorkflowExecutor
from workflow_orchestrator.schemas import Workflow


def test_executor_runs_dependencies_in_order():
    workflow = Workflow(
        workflow_id='wf1',
        name='test workflow',
        tasks=[
            {'task_id': 'a', 'name': 'Research', 'agent': 'research', 'payload': {'topic': 'monitoring'}},
            {'task_id': 'b', 'name': 'Analyze', 'agent': 'analysis', 'depends_on': ['a'], 'payload': {'source': 'a'}},
        ],
    )
    result = WorkflowExecutor().run(workflow)
    assert result.status == 'completed'
    assert [item.task_id for item in result.results] == ['a', 'b']


def test_executor_detects_unresolved_dependency():
    workflow = Workflow(
        workflow_id='wf2',
        name='bad workflow',
        tasks=[{'task_id': 'b', 'name': 'Blocked', 'depends_on': ['missing']}],
    )
    with pytest.raises(ValueError):
        WorkflowExecutor().run(workflow)
