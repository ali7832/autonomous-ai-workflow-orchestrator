# Autonomous AI Workflow Orchestrator

Production-ready workflow orchestration platform for AI automation systems, supporting task definitions, dependency-aware execution, agent assignment, workflow runs, APIs, CLI workflows, Docker, CI, and tests.

## Features

- Workflow and task schema definitions
- Dependency-aware DAG execution
- Specialized agent registry
- Run status tracking
- FastAPI orchestration API
- CLI demo and workflow execution commands
- JSON workflow example
- Docker and Docker Compose deployment
- GitHub Actions CI
- Pytest test suite
- Architecture and deployment documentation

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

## Docs

- `ARCHITECTURE.md`
- `DEPLOYMENT.md`
- `sample_workflow.json`

## Portfolio Highlights

- Demonstrates autonomous workflow orchestration and production API design
- Useful for agent systems, AI automation, ETL pipelines, and business process automation
- Strong foundation for queues, retries, schedules, human approvals, distributed workers, and LangGraph-style orchestration
