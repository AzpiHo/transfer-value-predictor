from fastapi.testclient import TestClient

from ftv_api.main import app
from ftv_api.mock import mock_delta
from ftv_api.schemas import Direction

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ftv-api"}


def test_prediction_matches_mock_and_sign() -> None:
    player_id = "11111111-1111-4111-8111-111111111111"
    response = client.get(f"/predictions/{player_id}")
    assert response.status_code == 200
    body = response.json()
    direction, delta = mock_delta(player_id)
    assert body["player_id"] == player_id
    assert body["horizon_months"] == 6
    assert body["direction"] == direction.value
    assert body["delta_value_eur"] == delta
    assert body["currency"] == "EUR"
    assert body["mocked"] is True
    assert body["label_source"] == "unconfigured"
    assert body["model_version"] == "stub-0.1.0"
    assert body["scope"]["leagues"] == [
        "EPL",
        "LA_LIGA",
        "SERIE_A",
        "BUNDESLIGA",
        "LIGUE_1",
    ]
    assert body["scope"]["competitions"] == ["UCL"]
    if body["direction"] == Direction.FLAT.value:
        assert body["delta_value_eur"] == 0
    elif body["direction"] == Direction.UP.value:
        assert body["delta_value_eur"] > 0
    else:
        assert body["delta_value_eur"] < 0
    assert body["delta_value_eur"] % 50_000 == 0


def test_prediction_is_stable() -> None:
    first = client.get("/predictions/sample-player").json()
    second = client.get("/predictions/sample-player").json()
    assert first == second


def test_rejects_unsafe_player_id() -> None:
    response = client.get("/predictions/bad_id")
    assert response.status_code == 422


def test_openapi_lists_prediction_routes() -> None:
    schema = client.get("/openapi.json").json()
    assert schema["info"]["title"] == "Transfer Value Prediction API"
    assert "/health" in schema["paths"]
    assert "/predictions/{player_id}" in schema["paths"]
    prediction = schema["components"]["schemas"]["Prediction"]
    assert "direction" in prediction["properties"]
    assert "delta_value_eur" in prediction["properties"]
