
# 🚗 Car Price Prediction — Production-Grade Machine Learning System

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-containerized-blue)
![MySQL](https://img.shields.io/badge/database-MySQL-orange)
![Scikit-learn](https://img.shields.io/badge/ML-scikit--learn-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A **production-style machine learning system** for predicting used car prices.

This project demonstrates how to build a **complete ML service**, moving beyond notebook experiments to a **deployable machine learning system** with:

* structured training pipelines
* artifact versioning
* FastAPI inference service
* prediction logging in a database
* containerized deployment

Unlike typical ML projects, this repository focuses on **machine learning system engineering**.

---


## 🚀Live Demo:
https://car-price-ml-system.onrender.com/

---

# 🎯 System Overview

The system predicts **used car selling prices** using a **Random Forest regression model** and exposes predictions through a **FastAPI API**.

Every prediction request is logged in a **MySQL database**, enabling monitoring and debugging of model behavior.

---

## ⚡ Quick Start

```bash
git clone https://github.com/Atharv-AC/Car-Price-ML-System.git
cd car-price-prediction
docker compose up --build


Open:
http://localhost:8000/docs

```


---

## 🔌 Example API Call

```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "mileage": 12,
  "engine": 234,
  "max_power": 123,
  "torque": 120,
  "km_driven_per_year": 200,
  "car_age": 2,
  "fuel": "CNG",
  "transmission": "Manual",
  "owner": "First Owner"
}'

```

---

# 📚 Table of Contents

* Overview
* System Highlights
* Key Features
* System Architecture
* Project Structure
* Prediction Request Lifecycle
* Model Training Pipeline
* Model Versioning
* Model Loading Strategy
* Inference API
* Database Logging
* API Endpoints
* Docker Deployment
* Design Decisions
* Technologies Used
* Running the Project
* Future Improvements
* Author

---

# 📌 Overview

Machine learning models trained in notebooks are not enough for real-world systems.

Production ML systems require:

* reproducible training pipelines
* model artifact management
* inference APIs
* monitoring and logging
* containerized deployment

This project demonstrates how to build such a **production-style ML service**.

The system separates **training** and **inference**, a key architectural principle in production ML.

---

# ⭐ System Highlights

- ✔ Training / Inference separation
- ✔ RandomForest regression model
- ✔ FastAPI inference service
- ✔ Prediction logging with MySQL
- ✔ SQLAlchemy ORM integration
- ✔ Docker containerization
- ✔ Docker Compose multi-service deployment

---

# 🚀 Key Features

* Machine learning model for **used car price prediction**
* Structured ML project architecture
* Reproducible training pipeline
* Model artifact versioning
* FastAPI inference API
* Database logging of predictions
* Containerized deployment with Docker
* Multi-container orchestration using Docker Compose

---

# 🏗 System Architecture

The system consists of **three major layers**.

---

## 1️⃣ ML Lifecycle

```
Dataset
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Model Artifact
```

<div align="center">
  <img src="docs/ML_System.png" width="800"/>
</div>

---

## 2️⃣ System Architecture

```
Client (Browser / Postman)
          ↓
      FastAPI API
          ↓
   Prediction Wrapper
          ↓
   RandomForest Model
          ↓
      SQLAlchemy
          ↓
      MySQL Database
```
<div align="center">
  <img src="docs/mermaid-diagram (4).png" width="500"/>
</div>

This architecture reflects a production-style ML inference system with validation, observability, and model lifecycle management.

The API performs inference and logs predictions into the database.

---

## 3️⃣ Deployment Architecture

```
Docker Compose

 ├── FastAPI Container
 │       ↓
 │   ML Model Inference
 │
 └── MySQL Container
         ↓
    Prediction Logging
```
<div align="center">
  <img src="docs/mermaid-diagram (3).png" width="900" />
</div>

This ensures **reproducible deployment environments**.

---

# 🔄 Prediction Request Lifecycle

1️⃣ User submits car features through API request.

2️⃣ FastAPI validates input using **Pydantic schemas**.

3️⃣ The prediction wrapper prepares the data.

4️⃣ The trained **RandomForest model** generates a prediction.

5️⃣ The prediction and input payload are stored in **MySQL**.

6️⃣ The API returns the predicted price to the client.

---

# UI Preview
### Home Page 
<img src="docs/image1.png" alt="Home page" width=600>
<img src="docs/image2.png" alt="Home page" width=600>

### About Page
<img src="docs/image3.png" alt="About page" width=600>
<img src="docs/image4.png" alt="About page" width=600>

---

# 📁 Project Structure

```
car-price-prediction/
│
├── 📄 Dockerfile                # Docker configuration for containerization
├── 📄 docker-compose.yml       # Multi-container setup (app + DB)
├── 📄 README.md                # Project documentation
├── 📄 requirements.txt         # Python dependencies
├── 📄 pyproject.toml           # Packaging & build configuration
│
├── 📂 data/                    # Raw and processed datasets
│   ├── Car_details.csv
│   ├── cleaned_car_data.csv
│   ├── cleaned_car_details.csv
│   └── cleaned_car_out.csv
│
├── 📂 models/                  # Trained models
│   ├── latest.joblib          # Latest production model
│   └── versions/              # Versioned models
│       └── rf_YYYYMMDD.joblib
│
├── 📂 reports/                 # Training & evaluation reports
│   ├── model_summary.json
│   └── train_summary.json
│
├── 📂 docs/                    # Architecture diagrams & documentation assets
│   ├── ML_System.png
│   └── mermaid-diagram.png
│
├── 📂 src/                     # Source code (main application)
│   └── car_price_prediction/
│       ├── __init__.py
│       ├── main.py            # Application entry point
│       ├── api.py             # API routes (FastAPI)
│       ├── config.py          # Config management
│       ├── config.yaml        # YAML-based configuration
│       ├── logger.py          # Logging utilities
│       ├── loader.py          # Data loading utilities
│       ├── train.py           # Training script
│       ├── predict.py         # Prediction logic
│
│       ├── 📂 pipeline/       # ML pipeline components
│       │   ├── preprocess.py  # Data preprocessing
│       │   ├── features.py    # Feature engineering
│       │   ├── train_model.py # Model training
│       │   └── evaluate.py    # Model evaluation
│
│       ├── 📂 database/       # Database layer
│       │   ├── connection.py  # DB connection setup
│       │   ├── models.py      # ORM models
│       │   └── repository.py  # DB operations
│
│       └── 📂 static/         # Frontend assets
│           ├── index.html
│           ├── style.css
│           ├── script.js
│           └── car-about.html
│
├── 📂 tests/                  # Unit & integration tests
│   ├── test_api_unit.py
│   ├── test_loader_unit.py
│   ├── test_predict_unit.py
│   ├── test_repository_unit.py
│   └── Integration/
│       └── test_mysql.py

```

The architecture separates:

* training pipeline
* inference service
* database operations
* configuration

---

# 🤖 Model Training Pipeline

The training pipeline performs the following steps:

1️⃣ Load cleaned dataset

2️⃣ Perform preprocessing and feature engineering

3️⃣ Train multiple regression models

* Linear Regression
* Ridge Regression
* Lasso Regression
* Random Forest

4️⃣ Perform hyperparameter tuning

5️⃣ Evaluate model performance

Metrics used:

```
R² Score
Mean Squared Error
Root Mean Squared Error
Mean Absolute Error
```

6️⃣ Save trained model artifact

---

# 🧠 Final Model

Best performing model:

```
RandomForestRegressor
```

Performance:

```
Training R²: ~96%
Testing R²: ~90%
RMSE: ~0.20
MAE: ~0.14

Note: Metrics are computed on normalized/log-transformed target values.
```

The trained pipeline is saved as:

```
models/latest.joblib
```

---

# 🧾 Model Versioning

- Every training run saves a timestamped model:
  models/versions/rf_20260312_183324.joblib

- latest.joblib is a symlink / copy of best model

- API always loads latest.joblib

This ensures:
- reproducibility
- rollback capability

---

# ⚙️ Model Loading Strategy

- Model is loaded at API startup
- Stored in memory for low-latency inference
- Avoids reloading per request

---

# 🧪 Testing

Includes:

- Unit Tests:
  - prediction logic
  - data loader
  - repository layer

- Integration Tests:
  - MySQL connection

Run tests:

pytest

---

# ⚡ Inference API

The inference service is implemented using **FastAPI**.

Responsibilities:

* load trained model at startup
* validate incoming requests
* generate predictions
* log predictions to database
* return API response

---

# 🗄 Database Logging

Every prediction request is logged in a **MySQL database**.

Table structure:

```
predictions
```

Columns:

```
id
timestamp
features (JSON)
predicted_price
model_version
```

Example record:

```
{
  "features": {...},
  "predicted_price": 536241,
  "model_version": "rf_latest"
}
```

This enables **prediction auditing and monitoring**.

---

# 🔌 API Endpoints

| Endpoint      | Method | Description                   |
| ------------- | ------ | ----------------------------- |
| `/health`     | GET    | Service health check          |
| `/predict`    | POST   | Generate car price prediction |
| `/model-info` | GET    | Metadata of deployed model    |

---

## Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

## Prediction Endpoint

```
POST /predict
```

Example request:

```json
{
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
```

Example response:

```json
{
  "Prediction": 536241
}
```

---

# 🐳 Docker Deployment

The system is containerized using **Docker**.

---

## Docker Compose (Recommended)

Run the full system:

```
docker compose up --build
```

Services started:

```
FastAPI API
MySQL Database
```

---

API available at:

```
http://localhost:8000
```

Interactive API docs:

```
http://localhost:8000/docs
```

---

# 🧠 Design Decisions

### Why a Prediction Wrapper?
- Decouples API layer from ML logic
- Allows swapping models without changing API
- Central place for preprocessing consistency

### Why RandomForest?
- Handles non-linearity
- Robust to outliers
- Minimal feature scaling required

### Why MySQL Logging?
- Enables auditability of predictions
- Supports future monitoring pipelines

---

# 🛠 Technologies Used

* Python
* Scikit-learn
* FastAPI
* Pydantic
* SQLAlchemy
* MySQL
* Docker
* Docker Compose

---

# ▶ Running the Project

### Clone repository

```
git clone https://github.com/Atharv-AC/Car-Price-ML-System.git
```

---

### Start system with Docker

```
docker compose up --build
```

---

### Open API documentation

```
http://localhost:8000/docs
```

---

# 🔮 Future Improvements

Possible enhancements:

* CI/CD pipeline
* ML experiment tracking (MLflow)
* model monitoring
* feature store integration
* cloud deployment

---

# 👨‍💻 Author

**Atharv Chandurkar**

Machine Learning Engineering Project

---

# ⭐ Why This Project Matters


This project focuses on **operationalizing ML**, not just training models.

It demonstrates how to move from:
- notebooks → production systems

with:
* reproducible training pipelines
* model artifact management
* API-based inference
* database logging
* containerized deployment

These practices reflect **real-world ML engineering workflows**.

