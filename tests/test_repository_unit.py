from car_price_prediction.database.repository import save_prediction
from car_price_prediction.database.models import Prediction
from car_price_prediction.database.connection import SessionLocal


def test_save_prediction():

    db = SessionLocal()

    features = {
        "mileage": 10,
        "engine": 1200,
        "max_power": 90,
        "torque": 200,
        "km_driven_per_year": 10000,
        "car_age": 3,
        "fuel": "Petrol",
        "transmission": "Manual",
        "owner": "First Owner"
    }

    record = save_prediction(
        session=db,
        features=features,
        price=500000,
        version="test_model_v1"
    )

    assert record.id is not None
    assert record.predicted_price == 500000
    assert record.model_version == "test_model_v1"

    db.close()


def test_prediction_saved_in_db():

    db = SessionLocal()

    features = {"mileage": 5}

    record = save_prediction(
        session=db,
        features=features,
        price=10000,
        version="v1"
    )

    result = db.query(Prediction).filter(Prediction.id == record.id).first()

    assert result is not None
    assert result.predicted_price == 10000

    db.close()