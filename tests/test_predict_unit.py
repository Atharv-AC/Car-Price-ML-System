import numpy as np
from car_price_prediction.predict import CarPriceModel
import pytest


# this is a fake model for testing prediction 
class FakeModel:
    def predict(self, df):
        return np.array([np.log(100000)])

# this is a fake model for testing prediction failure    
class BrokenModel:
    def predict(self, df):
        raise RuntimeError("Model failed")


valid_input_dict =  {
  "mileage": 12,
  "engine": 234,
  "max_power": 123,
  "torque": 120,
  "km_driven_per_year": 200,
  "car_age": 2,
  "fuel": "CNG",
  "transmission": "Manual",
  "owner": "First Owner"
}


# Checks for the model loading
def test_predict_success():
    model = CarPriceModel(FakeModel())
    result = model.predict(valid_input_dict)
    assert result == pytest.approx(100000)





# Using invalid input for all process is not worth
invalid_input_dict =  {
  "mileage": -12,
  "engine": 234,
  "max_power": 0,
  "torque": "fhd",
  "km_driven_per_year": 200,
  "car_age": 2,
  "fuel": "fndf",
  "transmission": 34,
  "owner": "First Owner"
}

# checks for model missing
def test_validation_failure():
    model = CarPriceModel(BrokenModel())

    with pytest.raises(RuntimeError):
        model.predict(valid_input_dict)
    

# checks for missing feature
def test_missing_feature():
    model = CarPriceModel(FakeModel())
    bad_input = valid_input_dict.copy()
    bad_input.pop("engine")
    
    with pytest.raises(ValueError):
        model.predict(bad_input)


# checks for unexpected feature
def test_unexpected_feature():
    model = CarPriceModel(FakeModel())
    bad_input = valid_input_dict.copy()
    bad_input["extra"] = 123
    with pytest.raises(ValueError):
        model.predict(bad_input)


# checks for numeric type
def test_numeric_type_failure():
    model = CarPriceModel(FakeModel())
    bad_input = valid_input_dict.copy()
    bad_input["torque"] = "abc"
    with pytest.raises(ValueError):
        model.predict(bad_input)


# checks for negative value
def test_negative_value():
    model = CarPriceModel(FakeModel())
    bad_input = valid_input_dict.copy()
    bad_input["mileage"] = -1

    with pytest.raises(ValueError):
        model.predict(bad_input)


# checks for invalid category
def test_invalid_category():
    model = CarPriceModel(FakeModel())
    bad_input = valid_input_dict.copy()
    bad_input["fuel"] = "maybe"

    with pytest.raises(ValueError):
        model.predict(bad_input)


def test_invalid_transmission():
    model = CarPriceModel(FakeModel())
    bad_input = valid_input_dict.copy()
    bad_input["transmission"] = "maybe"

    with pytest.raises(ValueError):
        model.predict(bad_input)


def test_invalid_owner():
    model = CarPriceModel(FakeModel())
    bad_input = valid_input_dict.copy()
    bad_input["owner"] = "maybe"

    with pytest.raises(ValueError):
        model.predict(bad_input)