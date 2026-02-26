# governance-analysis-engine

Analysis engine for Web3 governance data.

## Why

Governance proposals are long, unstructured, and difficult to evaluate consistently.  
This system processes structured proposal inputs and produces typed analytical outputs.

## Architecture

FastAPI application exposing synchronous endpoints.  
Business logic executed through typed service modules.

## Quick Start
```
pip install -e .[dev]
uvicorn governance_analysis_engine.main:app --reload
```

## License

[MIT License](LICENSE)