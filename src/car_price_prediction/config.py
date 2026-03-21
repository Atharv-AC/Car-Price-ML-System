from pydantic_settings import BaseSettings
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[2]    # Goes to the root of the project
MODEL_PATH = ROOT_DIR / "models" / "latest.joblib"
REPORT_PATH = ROOT_DIR / "reports" 

# print(ROOT_DIR)
# print(MODEL_PATH)
# print(REPORT_PATH)

class Settings(BaseSettings):
    app_env: str = "dev"                 #* dev, test, docker, prod this can be defined in .env and passed to the container
    log_level: str = "INFO"              
    model_path: str | None = None
    database_url: str | None = None     #* Database URL

    
    def get_model_path(self):
        if self.model_path:
            return self.model_path

        # Docker container networking
        if self.app_env == "docker":
            return "/app/models/latest.joblib"

        # Local machine (for pytest or local dev)
        return "models/latest.joblib"
    
    def get_database_url(self):
        # 1. FIRST priority → environment variable (Render)
        env_db = os.getenv("DATABASE_URL")
        if env_db:
            return env_db
        
        # 2. If passed via pydantic settings
        if self.database_url:
            return self.database_url

        # 3. Docker container networking
        if self.app_env == "docker":
            return "mysql+pymysql://root:password123@db:3306/car_price_db"

        # 4. Local machine (for pytest or local dev)
        return "mysql+pymysql://root:password123@localhost:3307/car_price_db"
    

settings = Settings()