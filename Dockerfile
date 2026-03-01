FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/

RUN pip install --no-cache-dir .

EXPOSE 5577

CMD ["uvicorn", "governance_analysis_engine.main:app", "--host", "0.0.0.0", "--port", "5577"]
