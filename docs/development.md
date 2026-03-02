# Development Guide

## Quick Start

```bash
pip install -e .[dev]
uvicorn governance_analysis_engine.main:app --reload
```

## Docker

Build and run with a single command:

```bash
docker build -t governance-analysis-engine . && docker run -p 5577:5577 governance-analysis-engine
```

Or use the Makefile:

```bash
make build   # build the image
make run     # run the container
make up      # build + run
make stop    # stop the container
```

The API will be available at `http://localhost:5577`.

## Running Tests

```bash
pytest
```

## Lint & Type Check

```bash
ruff check .
mypy src/ --strict
```
