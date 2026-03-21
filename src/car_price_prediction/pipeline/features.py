from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[3] # Goes to the root of the project
DATA_DIR = BASE_DIR / "data"



def load_csv():
    return pd.read_csv(DATA_DIR / "cleaned_car_out.csv")

df = load_csv()
def build_preprocessor(df):
    # Separate features
    # features are the columns which not contain only price column but all other columns
    # axis=1 means columns axis is 1 i.e. columns are the features and price is the target
    features = df.drop(["selling_price" , "name", "seats", "seller_type"], axis=1)
    # print(features.columns)
    # Separate target
    # log transform stabilized variance
    target = np.log(df["selling_price"])

    numerical_cols = [
        "mileage",
        "engine",
        "max_power",
        "torque",
        "km_driven_per_year",
        "car_age"
    ]

    categorical_cols = [
        "fuel",
        "transmission",
        "owner"
    ]


    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )


    return features, target, preprocessor


