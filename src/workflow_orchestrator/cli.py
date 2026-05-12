import json
from pathlib import Path

import typer
from rich.console import Console

from workflow_orchestrator.executor import WorkflowExecutor
from workflow_orchestrator.schemas import Workflow

app = typer.Typer(help='Autonomous AI workflow orchestrator CLI')
console = Console()


@app.command()
def run(path: Path = Path('sample_workflow.json')) -> None:
    workflow = Workflow(**json.loads(path.read_text(encoding='utf-8')))
    result = WorkflowExecutor().run(workflow)
    console.print_json(data=result.model_dump())


@app.command()
def demo() -> None:
    workflow = Workflow(
        workflow_id='demo-workflow',
        name='Demo Research Workflow',
        tasks=[
            {'task_id': 'research', 'name': 'Research topic', 'agent': 'research', 'payload': {'topic': 'AI monitoring'}},
            {'task_id': 'analysis', 'name': 'Analyze findings', 'agent': 'analysis', 'depends_on': ['research'], 'payload': {'source': 'research'}},
            {'task_id': 'report', 'name': 'Generate report', 'agent': 'reporting', 'depends_on': ['analysis'], 'payload': {'sections': ['summary', 'recommendations']}},
        ],
    )
    result = WorkflowExecutor().run(workflow)
    console.print_json(data=result.model_dump())
