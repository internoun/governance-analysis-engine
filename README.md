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

## Development

See [docs/development.md](docs/development.md) for setup instructions.

## License

[MIT License](LICENSE)
