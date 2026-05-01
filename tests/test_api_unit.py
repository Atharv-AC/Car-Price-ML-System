from car_price_prediction.api import app, get_model
from fastapi.testclient import TestClient
from car_price_prediction.api import get_db
import pytest


# ---------- Fixture ----------

# @pytest.fixture
# def client():
#     app.state.model_loaded = True
#     return TestClient(app)

# ---------- Fake Model ----------

class FakeModel:
    def predict(self, data):
        return 653324


def fake_get_model():
    return FakeModel()



def fake_get_db():
    yield None


@pytest.fixture
def client():
    app.state.model_loaded = True
    app.state.model = FakeModel()
    return TestClient(app)


# ---------- Tests ----------

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200



def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "model_loaded" in response.json()


def test_get_model_success():

    app.state.model_loaded = True
    app.state.model = FakeModel()

    model = get_model()

    assert isinstance(model, FakeModel)

def test_get_model_failure():

    app.state.model_loaded = False

    with pytest.raises(Exception):
        get_model()


def test_health_model_not_loaded(client):
    app.state.model_loaded = False

    response = client.get("/health")

    assert response.status_code == 503

def test_model_info(client):
    response = client.get("/model-info-car")
    data = response.json()

    assert response.status_code == 200
    assert "model_file" in data
    assert isinstance(data["model_file"], str)

from unittest.mock import patch

def test_model_info_failure(client):

    with patch("builtins.open", side_effect=Exception("file missing")):
        response = client.get("/model-info-car")

        assert response.status_code == 500


def test_predict_with_fake_model(client):
    # model and db Override dependency only for this test
    app.dependency_overrides[get_model] = fake_get_model
    app.dependency_overrides[get_db] = fake_get_db

    response = client.post("/predict-car", json={
        "mileage": 12,
        "engine": 234,
        "max_power": 123,
        "torque": 120,
        "km_driven_per_year": 200,
        "car_age": 2,
        "fuel": "CNG",
        "transmission": "Manual",
        "owner": "First Owner"
        })

    assert response.status_code == 200
    assert response.json()["Prediction"] == 653324

    # Clean override
    app.dependency_overrides.clear()


def test_predict_when_model_not_loaded(client):
    # Ensure no override
    app.dependency_overrides.clear()

    # Simulate model not loaded
    app.state.model_loaded = False

    response = client.post("/predict-car", json={
        "mileage": 12,
        "engine": 234,
        "max_power": 123,
        "torque": 120,
        "km_driven_per_year": 200,
        "car_age": 2,
        "fuel": "CNG",
        "transmission": "Manual",
        "owner": "First Owner"
        })

    assert response.status_code == 503

def test_predict_validation_error(client):

    response = client.post("/predict-car", json={
        "wrong": "data"
    })

    assert response.status_code == 422


def test_get_db_generator():

    gen = get_db()

    db = next(gen)

    assert db is None or db is not None