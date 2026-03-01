# governance-analysis-engine

Analysis engine for Web3 governance data.

## Why

Governance proposals are long, unstructured, and difficult to evaluate consistently.
This system processes structured proposal inputs and produces typed analytical outputs.

## Architecture

Layered backend: API → Middleware → Service → Client. See [docs/architecture.md](docs/architecture.md) for details.

## Project Structure

```
src/governance_analysis_engine/
├── main.py                # FastAPI application
├── config.py              # Logging configuration
├── exceptions.py          # Custom exceptions
├── clients/               # External API clients
├── middleware/            # Error handling
└── services/              # Business logic
```

## API Usage

### Health Check

```
GET /health
```

```json
{ "status": "ok" }
```

### Proposal Summary

```
POST /proposal/summarize
```

```json
{ "message": "Summarized proposal text..." }
```

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

## License

[MIT License](LICENSE)
