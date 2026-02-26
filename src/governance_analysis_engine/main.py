from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class HealthResponse(BaseModel):
    status: str


class MessageResponse(BaseModel):
    message: str


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/info", response_model=MessageResponse)
def get_info() -> MessageResponse:
    return MessageResponse(message="governance-analysis-engine running")
