from sqlalchemy import Column, Integer, String, JSON, DateTime, Float
from car_price_prediction.database.connection import Base
from datetime import datetime, UTC


# Creating a table in the database name "predictions"
class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now(UTC))
    features = Column(JSON)
    predicted_price = Column(Float)
    model_version = Column(String(100))