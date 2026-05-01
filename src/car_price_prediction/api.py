from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from car_price_prediction.config import settings
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
from fastapi import BackgroundTasks



def wait_for_db(engine, retries=10, delay=3):
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
class Car(BaseModel):
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
from threading import Thread

@asynccontextmanager
async def lifespans(app: FastAPI):

    # -----------------------------------------
    # Step 1: Initialize app state
    # -----------------------------------------
    # This stores model in memory (shared across requests)
    app.state.model_loaded = False
    app.state.model = None


    # -----------------------------------------
    # Step 2: Define background function
    # -----------------------------------------
    def load_model_in_background():
        """
        This function runs in a SEPARATE THREAD.

        Why?
        - So app can start instantly
        - Model loads without blocking startup
        """

        try:
            # Import inside function to avoid slow startup
            from car_price_prediction.loader import load_model
            from car_price_prediction.predict import CarPriceModel

            # Load trained ML model from disk
            model = load_model()

            # Wrap model (your prediction wrapper)
            app.state.model = CarPriceModel(model)

            # Mark model as ready
            app.state.model_loaded = True

            logger.info("✅ Model loaded successfully in background")

        except Exception:
            logger.error("❌ Model failed to load", exc_info=True)


    # -----------------------------------------
    # Step 3: Start background thread
    # -----------------------------------------
    Thread(target=load_model_in_background, daemon=True).start() # daemon=True ensures thread doesn't block shutdown

    # 👉 This line is KEY:
    # It allows FastAPI to continue startup WITHOUT waiting


    # -----------------------------------------
    # Step 4: Setup database (non-blocking)
    # -----------------------------------------
    try:
        wait_for_db(engine, retries=10, delay=1)
        Base.metadata.create_all(bind=engine)
        logger.info("Database ready")
    except:
        logger.warning("Database not available, continuing...")


    # -----------------------------------------
    # Step 5: Yield control to FastAPI
    # -----------------------------------------
    yield

    # Runs on shutdown
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
        raise HTTPException(status_code=503, detail="Model is still loading, please try again in a few seconds")
    return app.state.model


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


# with open(REPORT_DIR, "r") as f:
#     data = json.load(f)

# Load model metadata (like model version info) once at startup
with open(REPORT_DIR) as f:
    MODEL_METADATA = json.load(f)



def save_prediction_task(features, price, version):

    # This function runs in the background AFTER response is sent

    # Create a NEW DB session (important: request DB is already closed)
    db = SessionLocal()

    try:
        # Save prediction details into database
        save_prediction(
            session=db,
            features=features,
            price=price,
            version=version
        )

    except Exception as e:
        # If DB write fails, log error (but DO NOT crash API)
        logger.error(f"Background DB save failed: {e}", exc_info=True)

    finally:
        db.close()



@app.post("/predict-car")
def predict_price(features: Car, background_tasks: BackgroundTasks, model = Depends(get_model)): # dependincy injection for model


    # * Convert validated Pydantic model to dict before passing into model wrapper.
    price = model.predict(features.model_dump())
    input_data = features.model_dump()

 
    try:
       if settings.app_env != "test":
        background_tasks.add_task(         #* here background_tasks.add_task(func, arg1, arg2, arg3)
                save_prediction_task,      #* is equivalent to func(arg1, arg2, arg3)  
                input_data,                             #* means save_prediction_task(input_data, price, MODEL_METADATA)
                float(price),
                str(MODEL_METADATA)
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
            "model_loaded": app.state.model_loaded
            }


# get request for model metadata it will not return anything if the model is not loaded
@app.get("/model-info-car")
def load_model_metadata():
    from pathlib import Path
    
    # * Runtime metadata written during training; used for quick model introspection.
    REPORT_PATH = Path("reports/train_summary.json")

    try:
        with open(REPORT_PATH) as fi:
            model_summary = json.load(fi)
            model_summary["model_file"] = str(settings.get_model_path())

            return model_summary
        
    except Exception:
        logger.error("Model Metadata failed to load: ", exc_info=True)
        # 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Model Metadata not found")



@app.get("/predictions-car")
def get_predictions(db = Depends(get_db)):

    from car_price_prediction.database.models import Prediction

    # * Return the last 10 predictions
    records = db.query(Prediction).order_by(Prediction.id.desc()).limit(10).all()

    # * Convert to JSON with only price and timestamp
    return [
        {
            "price": r.predicted_price,
            "timestamp": r.timestamp,
            **r.features   # unpack all features
        }
        for r in records
    ]

# {"mileage": 18.0, "engine": 1000.0, "max_power": 60.0, "torque": 100.0, "km_driven_per_year": 8000.0, "car_age": 15.0, "fuel": "Petrol", "transmission": "Automatic", "owner": "First Owner"}
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



#? Flow Before:
# Request → Prediction → DB Save → Response


#? Flow Now:
# Request → Prediction → Response (fast)
#                           ↓
#                    DB Save (background)

# ✅ User doesn’t wait
# ✅ System feels faster

