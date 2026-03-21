from pathlib import Path
import pandas as pd
import joblib
from car_price_prediction.config import settings
from car_price_prediction.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2] # Goes to the root of the project
print(BASE_DIR)
DATA_DIR = BASE_DIR / "data"
print(DATA_DIR)



def load_csv():
    return pd.read_csv(DATA_DIR / "cleaned_car_out.csv")


# df = load_csv()

# a = df.info()
# b = df.describe()
# print(a)
# print(df.iloc[1:10, 5:].describe())

def save_model(model, model_path: Path):
    joblib.dump(model, model_path)


def load_model():
    logger.info("Loading model from disk")
    return joblib.load(settings.get_model_path())