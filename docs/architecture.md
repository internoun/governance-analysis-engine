# Architecture

## Layered Design

The application follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                         API Layer                            │
│                      (FastAPI Routes)                        │
│  /health, /info, /proposal/summarize                        │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Middleware Layer                        │
│                   (Error Handling, Logging)                  │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                           │
│              (Business Logic & Domain Models)                │
│           Proposal, ProposalSummary, analysis                │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                           │
│              (External Data Integration)                     │
│              DataClient for API calls                        │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Layer    | Component               | Responsibility                            |
|----------|-------------------------|-------------------------------------------|
| API      | main.py                 | Route definitions, request/response models |
| Middleware | error_handler.py      | Centralized exception handling            |
| Service  | proposal_service.py     | Proposal analysis, domain models          |
| Client   | data_client.py          | External API communication                |
| Config   | config.py               | Logging configuration                     |

## Request Flow

1. HTTP request arrives at FastAPI route
2. Middleware intercepts for error handling
3. Service layer processes business logic
4. Client layer fetches external data if needed
5. Response propagates back through layers
