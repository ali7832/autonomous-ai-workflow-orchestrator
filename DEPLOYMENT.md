# Deployment Guide

## Local Development

```bash
pip install .[dev]
uvicorn workflow_orchestrator.api:app --reload
```

## CLI Demo

```bash
workflowctl demo
workflowctl run sample_workflow.json
```

## Docker

```bash
docker build -t workflow-orchestrator .
docker run -p 8000:8000 workflow-orchestrator
```

## Docker Compose

```bash
docker-compose up --build
```

## Health Check

```bash
curl http://localhost:8000/health
```

## Run Workflow

```bash
curl -X POST http://localhost:8000/workflows/run \
  -H 'Content-Type: application/json' \
  -d @sample_workflow.json
```
