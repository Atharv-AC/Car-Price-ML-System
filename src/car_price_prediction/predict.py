import numpy as np
import pandas as pd



# * feature set expected by the trained pipeline.
required_features = [
  "mileage",
  "engine",
  "max_power",
  "torque",
  "km_driven_per_year",
  "car_age",
  "fuel",
  "transmission",
  "owner"
]



class CarPriceModel:
    def __init__(self, model):
        self.model = model
    
    def validate(self, input_dict: dict):
        """
        handles missing or unexpected features
        """
        # ! raise error if any required feature is missing; model expects full schema.
        missing = [f for f in required_features if f not in input_dict]

        if missing:
            raise ValueError(f"Missing required features: {missing}")

        # ! Reject unknown fields to avoid silently ignoring bad payloads.
        for f in input_dict:
            if f not in required_features:
                raise ValueError(f"Unexpected feature: {f}")
            
        # * Validate numerical features
        num_feature = ["mileage","engine","max_power","torque","km_driven_per_year","car_age"]

        for f in num_feature:
            try:
                input_dict[f] = float(input_dict[f])
            except:
                raise ValueError(f"{f} must be a number")
            
            if input_dict[f] < 0:
                raise ValueError(f"{f} Cannot be negative")

        # * Validate categorical features exactly as used during training.
        fuel_feature = ["fuel"]

        for f in fuel_feature:
            if input_dict[f] not in ['Diesel', 'Petrol', 'LPG', 'CNG']:
                raise ValueError(f"{f} must be one of the following ['Diesel', 'Petrol', 'LPG', 'CNG']")

        transmission_feature = ["transmission"]

        for f in transmission_feature:
            if input_dict[f] not in ['Automatic', 'Manual']:
                raise ValueError(f"{f} must be one of the following ['Automatic', 'Manual']")

        owner_feature = ["owner"]

        for f in owner_feature:
            if input_dict[f] not in ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner']:
                raise ValueError(f"{f} must be one of the following ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner']")
            
        return input_dict
        
    def to_dataframe(self, input_dict: dict):
        return pd.DataFrame([input_dict])


    def predict(self, input_dict: dict) -> float:
        validate_input = self.validate(input_dict)
        df = self.to_dataframe(validate_input)
        log_pred = self.model.predict(df)

        # * Model predicts log(price), so convert back to actual price.
        price = np.exp(log_pred)
        return float(price[0])
