import yaml

def load_config():
    import os
    #  Resolve config relative to this module so training works from any CWD.
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, "config.yaml")


    with open(config_path, "r") as fi:
         config = yaml.safe_load(fi)

    return config

config = load_config()


def train_randomforest_model(config):
        from car_price_prediction.logger import get_logger
        logger = get_logger(__name__)

        from datetime import datetime, timezone
        import json
        from pathlib import Path

        #  Project root inferred from src/car_price_prediction/train.py -> ../../
        BASE_DIR = Path(__file__).resolve().parents[2]
        MODELS_DIR = BASE_DIR / "models"
        VERSIONS_DIR = MODELS_DIR / "versions"
        REPORTS_DIR = BASE_DIR / "reports"

        #  Ensure output directories exist.
        MODELS_DIR.mkdir(exist_ok=True)
        VERSIONS_DIR.mkdir(exist_ok=True)
        REPORTS_DIR.mkdir(exist_ok=True)
 

        save_path = REPORTS_DIR /"train_summary.json"
        save_model_path = REPORTS_DIR / "model_summary.json"


        #  Training split settings are controlled centrally via config.yaml.
        test_size = config["train"]["test_size"]
        randomstate = config["train"]["random_state"]
        

        from car_price_prediction.loader import load_csv, save_model
        from car_price_prediction.pipeline.features import build_preprocessor
        from sklearn.model_selection import train_test_split
        from car_price_prediction.pipeline.train_model import model_rf

        df = load_csv()

        logger.info("Training started")

        features, target, preprocessor = build_preprocessor(df)


        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=test_size, random_state=randomstate
            )

        model, _, best_params, cv_scores, r2, Tr2 = model_rf(preprocessor, X_train, y_train, X_test, y_test)
        
        time_stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        model_filename = f"rf_{time_stamp}.joblib"
        verions_filename = "latest.joblib"

        verions_path = VERSIONS_DIR / model_filename
        models_path = MODELS_DIR / verions_filename
        
        #  Save both immutable versioned artifact and mutable latest pointer.
        save_model(model, verions_path)
        save_model(model, models_path)


        model_summary = {
              "model_file": model_filename
        }

        logger.info("Best alpha: %s", best_params)
        logger.info("Best CV score: %s", cv_scores)
        logger.info("Test R2: %s", r2)
        logger.info("Training R2: %s", Tr2)

        summary = {
            "model_type": "rf",
            "best_alpha": best_params,
            "cv_score": cv_scores,
            "test_r2": r2,
            "train_r2": Tr2,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
            
        #  Persist run metrics for experiment tracking/debugging.
        with open (save_path, "w") as file:
            json.dump(summary, file, indent=4)

        logger.info("Training completed")

        #  Persist current model filename for inference-time lookup.
        with open(save_model_path, "w") as file:
              json.dump(model_summary, file, indent=4)
            
        logger.info("Model saved successfully")


if __name__ == "__main__":
    train_randomforest_model(config)

