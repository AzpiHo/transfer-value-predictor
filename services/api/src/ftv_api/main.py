"""FastAPI application for mocked transfer-value predictions."""

import os
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ftv_api.mock import mock_prediction
from ftv_api.schemas import Health, Prediction

PLAYER_ID_PATTERN = re.compile(r"^[A-Za-z0-9-]{1,64}$")

app = FastAPI(
    title="Transfer Value Prediction API",
    version="0.1.0",
    summary="Mocked 6-month change in player market value.",
    description=(
        "Predicts the direction and magnitude of Δ market value over six months "
        "for players in the Big 5 leagues, with the Champions League in scope. "
        "Responses are mocked. This service does not read a valuation feed and "
        "does not call an external football API."
    ),
)

_origins = [
    origin.strip()
    for origin in os.environ.get("WEB_ORIGIN", "http://localhost:3000").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health", response_model=Health, tags=["meta"])
def health() -> Health:
    return Health(status="ok", service="ftv-api")


@app.get(
    "/predictions/{player_id}",
    response_model=Prediction,
    tags=["predictions"],
)
def get_prediction(player_id: str) -> Prediction:
    if PLAYER_ID_PATTERN.fullmatch(player_id) is None:
        raise HTTPException(
            status_code=422,
            detail="player_id must be 1-64 characters: letters, digits, and hyphens.",
        )
    return mock_prediction(player_id)


def main() -> None:
    import uvicorn

    port = int(os.environ.get("API_PORT", "8000"))
    uvicorn.run("ftv_api.main:app", host="0.0.0.0", port=port)
