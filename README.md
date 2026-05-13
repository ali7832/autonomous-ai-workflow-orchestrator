# Autonomous AI Workflow Orchestrator

Deployable workflow automation platform for AI and operations workloads. It executes dependency-aware task DAGs, assigns tasks to agents, returns run metadata, and stores workflow run events for demo and audit workflows.

## Core Capabilities

- Workflow and task schema definitions
- Dependency-aware DAG execution
- Specialized agent registry
- Workflow run IDs for traceability
- Task-level duration and dependency metadata
- Run-level total duration, status, environment, and orchestrator version
- JSONL workflow run event stream for local audit/demo mode
- FastAPI `/workflows/run` API
- CLI demo and workflow execution commands
- Runtime configuration through environment variables
- Docker and Docker Compose deployment
- GitHub Actions CI
- Pytest coverage
- Operations runbook and architecture decision record

## Quickstart

```bash
pip install .[dev]
workflowctl demo
uvicorn workflow_orchestrator.api:app --reload
pytest -q
```

## API

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/workflows/run \
  -H 'Content-Type: application/json' \
  -d @sample_workflow.json
```

## Docker

```bash
docker-compose up --build
```

## Runtime Configuration

See `.env.example` for environment, orchestrator version, run store path, task timeout, and workflow size settings.

## Documentation

- `ARCHITECTURE.md`
- `DEPLOYMENT.md`
- `OPERATIONS.md`
- `docs/adr-001-workflow-run-service.md`
- `sample_workflow.json`

## Production Roadmap

- Persistent workflow database
- Queue-backed distributed workers
- Retry policies and dead-letter queues
- Human approval gates
- Scheduled workflow runs
- LangGraph or agent framework integration
- Web dashboard for run history and task timelines
