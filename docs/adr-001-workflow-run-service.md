# ADR-001: Workflow Run Service and Execution Metadata

## Status

Accepted

## Context

Workflow automation systems need more than a task executor. Operators need run IDs, task duration, dependency visibility, execution status, orchestrator version, and a run event stream that can support audits, demos, and future dashboards.

## Decision

Introduce a `WorkflowOrchestrationService` that owns workflow execution, health metadata, run persistence, and deployable API behavior. The executor records run-level and task-level metadata while preserving dependency-aware execution.

## Consequences

Benefits:

- FastAPI routes remain thin and deployable.
- Every workflow execution receives a traceable run ID.
- Task durations and dependencies are visible in API responses.
- JSONL run storage supports local demos and simple audit trails.
- The architecture can evolve into distributed workers and scheduled workflows.

Tradeoffs:

- Current execution is synchronous and local.
- Production deployments should add queues, retries, database persistence, and worker isolation.
