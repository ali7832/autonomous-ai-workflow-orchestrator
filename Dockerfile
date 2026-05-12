FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src

RUN pip install --upgrade pip && pip install .

EXPOSE 8000

CMD ["uvicorn", "workflow_orchestrator.api:app", "--host", "0.0.0.0", "--port", "8000"]
