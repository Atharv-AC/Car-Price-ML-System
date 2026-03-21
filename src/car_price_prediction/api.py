from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from car_price_prediction.loader import load_model
from contextlib import asynccontextmanager
from car_price_prediction.config import settings
from car_price_prediction.predict import CarPriceModel
from car_price_prediction.logger import get_logger
from car_price_prediction.database.connection import SessionLocal, engine, Base
from car_price_prediction.database.repository import save_prediction
logger = get_logger(__name__)
import json
from pathlib import Path
import time
from sqlalchemy.exc import OperationalError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware




def wait_for_db(engine, retries=1, delay=3):
    """
    Wait until the database becomes available.
    Prevents startup race condition in Docker.
    """
    for i in range(retries):
        try:
            with engine.connect() as conn:
                logger.info("Database connection successful")
                return
        except OperationalError:
            logger.warning(f"Database not ready... retry {i+1}/{retries}")
            time.sleep(delay)

    raise Exception("Database never became ready")





BASE_DIR = Path(__file__).resolve().parents[2] # Goes to the root of the project
REPORT_DIR = BASE_DIR / "reports/model_summary.json"






# * Request body schema expected by the prediction endpoint.
class car(BaseModel):
    mileage: float
    engine: float
    max_power: float
    torque: float
    km_driven_per_year: float
    car_age: float
    fuel: str
    transmission: str
    owner: str

# lifespan will run before the first request. It is used to load the model and save it in app state
@asynccontextmanager
async def lifespans(app: FastAPI):

    # always define state variables first
    app.state.model_loaded = False
    app.state.model = None
    

    # ✅ Load model FIRST (independent)
    try:
        # * Load and wrap the trained model once during startup.
        model = load_model()
        app.state.model = CarPriceModel(model)
        app.state.model_loaded = True
        logger.info("Model loaded successfully")

    except Exception:
        # exc_info=True will log the full traceback
        logger.error("Model failed to load: ", exc_info=True)


    # ✅ Load database SECOND (dependent)
    try:
        wait_for_db(engine)
        Base.metadata.create_all(bind=engine)
        logger.info("Database ready")
    except Exception:
        logger.warning("Database not available, continuing without DB")

    yield

    logger.info("Shutting down")

app = FastAPI(lifespan=lifespans)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# This tells FastAPI: /static/* → serve files from static folder
# http://localhost:8000/static/style.css
app.mount("/static", StaticFiles(directory="src/car_price_prediction/static"), name="static")


@app.get("/")
def home():
    return FileResponse("src/car_price_prediction/static/index.html")





# @app.get("/")
# def read_root():
#     return {"message": "helasdfghjrld"}





def get_model():
    # ! Dependency guard: inference endpoints should fail first until model is ready.
    if not app.state.model_loaded:
        # 503 Service Unavailable
        raise HTTPException(status_code=503, detail="Model not loaded")
    return app.state.model


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


# with open(REPORT_DIR, "r") as f:
#     data = json.load(f)


@app.post("/predict-car")
def predict_price(features: car, model = Depends(get_model), db = Depends(get_db)): # dependincy injection for database and model


    # * Convert validated Pydantic model to dict before passing into model wrapper.
    price = model.predict(features.model_dump())
    input_data = features.model_dump()

    MODEL_METADATA = json.load(open(REPORT_DIR))
 
    try:
       if db and settings.app_env != "test":
        save_prediction(
            session=db,
            features=input_data,
            price=float(price),
            version=str(MODEL_METADATA)
        )

    except Exception:
        # logger.warning("Failed to save prediction to DB", exc_info=True)
        logger.warning("Database not available, skipping save")

    
    return {'Prediction' : float(price)}


# get request for health check it ensures that the model is loaded and returns a true/false
@app.get("/health")
def health_info():
    if not app.state.model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
            "status": "ok",
            "model_loaded": True
            }


# get request for model metadata it will not return anything if the model is not loaded
@app.get("/model-info")
def load_model_metadata():
    from pathlib import Path
    
    # * Runtime metadata written during training; used for quick model introspection.
    REPORT_PATH = Path("reports/model_summary.json")

    try:
        with open(REPORT_PATH) as fi:
            model_summary = json.load(fi)
            return model_summary
    except Exception:
        logger.error("Model Metadata failed to load: ", exc_info=True)
        # 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Model Metadata not found")


# {
#   "mileage": 12,
#   "engine": 234,
#   "max_power": 123,
#   "torque": 120,
#   "km_driven_per_year": 200,
#   "car_age": 2,
#   "fuel": "CNG",
#   "transmission": "Manual",
#   "owner": "First Owner"
# }
