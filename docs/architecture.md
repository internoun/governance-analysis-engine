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
│                     Repository Layer                         │
│              (Data Access Abstraction)                       │
│           ProposalRepository, InMemoryProposalRepository     │
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
| Repository | proposal_repository.py | Data access abstraction                   |
| Client   | data_client.py          | External API communication                |
| Config   | config.py               | Logging configuration                     |

## Request Flow

1. HTTP request arrives at FastAPI route
2. Middleware intercepts for error handling
3. Service layer processes business logic
4. Repository layer handles data access (add/get proposals)
5. Client layer fetches external data if needed
6. Response propagates back through layers

## Repository Pattern

The repository layer provides a data access abstraction using a Protocol-based interface:

- `ProposalRepository`: Protocol defining the contract for proposal data access
- `InMemoryProposalRepository`: In-memory implementation for current use case
- Services depend on the Protocol, enabling easy substitution of implementations

This design supports testing (mock repositories) and future persistence layers (database, cache, etc.) without modifying service logic.
