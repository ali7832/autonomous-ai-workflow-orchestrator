# Operations Runbook

## Purpose

This service executes dependency-aware AI and automation workflows through a deployable API and CLI interface.

## Runtime Configuration

Configuration is controlled through `.env.example`:

- `WORKFLOW_ENV`: deployment environment.
- `WORKFLOW_SERVICE_NAME`: service identifier.
- `WORKFLOW_ORCHESTRATOR_VERSION`: executor version returned in workflow runs.
- `WORKFLOW_RUN_STORE_PATH`: JSONL workflow run event path.
- `WORKFLOW_DEFAULT_TASK_TIMEOUT_SECONDS`: default task timeout for future worker implementations.
- `WORKFLOW_MAX_TASKS_PER_WORKFLOW`: maximum allowed workflow size.

## Workflow Lifecycle

1. A workflow definition is submitted to `/workflows/run`.
2. The service creates a workflow run ID.
3. Tasks are executed when their dependencies are satisfied.
4. Each task result records agent name, status, output, dependencies, and duration.
5. The workflow run records total duration and orchestrator version.
6. The run is persisted to the JSONL event stream.

## Demo Readiness

Expose `/health` and `/workflows/run`. Health returns service name, environment, and orchestrator version.

## Production Roadmap

- Persistent run database.
- Queue-backed distributed workers.
- Retry policies and dead-letter queues.
- Human approval gates.
- Scheduled workflow runs.
- LangGraph or agent framework integration.
- Web dashboard for run history and task timelines.
