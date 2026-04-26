
# 🚗 Car Price Prediction — Production-Grade Machine Learning System


![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-containerized-blue)
![MySQL](https://img.shields.io/badge/database-MySQL-orange)
![Scikit-learn](https://img.shields.io/badge/ML-scikit--learn-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Tests](https://img.shields.io/badge/tests-89%25-green)

A **production-grade machine learning system** for predicting used car prices,
designed to demonstrate **real-world ML system design, deployment, and reliability**.
---

## 🚀 Live Demo

👉 [https://car-price-ml-system.onrender.com/](https://car-price-ml-system.onrender.com/)

---


## 📌 Overview

Most ML projects stop at notebooks.

This project goes beyond typical ML workflows — implementing a **complete, deployable ML system** with:

* structured training pipelines
* model versioning
* API-based inference (FastAPI)
* database logging for predictions
* containerized deployment (Docker)

It demonstrates how real-world ML systems are built, deployed, and maintained.

> ⚡ This project is designed to reflect how ML systems are built in production — not just how models are trained.

---

## 🎯 Use Case

Predict the selling price of used cars based on:
- vehicle specifications
- usage patterns
- ownership details

Useful for:
- resale platforms
- price estimation tools
- dealership analytics

---


## 💡 What This Project Demonstrates

This project goes beyond typical ML workflows and focuses on **production-grade machine learning engineering**.

It demonstrates:

- End-to-end ML system design — from data processing to deployment  
- Clear separation of **training and inference pipelines**  
- Model versioning with reproducibility and rollback capability  
- Deployment of ML models as a **FastAPI service**  
- Persistent prediction logging for monitoring and debugging  
- Backend design patterns (repository pattern, dependency injection)  
- Containerized deployment using Docker and Docker Compose  
- Testing across API, database, and ML pipeline components  

Unlike typical ML projects:

- Not limited to Jupyter notebooks  
- Emphasizes **system design over just model performance**  
- Built with **production constraints and reliability in mind**  

👉 This project reflects how real-world ML systems are **designed, deployed, and maintained in production environments**.

---

## ⚡ Quick Start

```bash
git clone https://github.com/Atharv-AC/Car-Price-ML-System.git
cd Car-Price-ML-System
docker compose up --build


Open:
http://localhost:8000/docs

```


---

## ⚙️ Environment Configuration

Create a `.env` file:

```env
APP_ENV=dev
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/car_price_db
```

### Environment Modes

| Environment | DATABASE_URL        |
| ----------- | ------------------- |
| Local       | localhost           |
| Docker      | db                  |
| Testing     | sqlite:///./test.db |

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

# ⭐ System Highlights

- ✔ Training / Inference separation
- ✔ RandomForest regression model
- ✔ FastAPI inference service
- ✔ Prediction logging with MySQL
- ✔ SQLAlchemy ORM integration
- ✔ Docker containerization
- ✔ Docker Compose multi-service deployment

---



# 🏗 System Architecture

The system is organized into **three layers**:

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

## 🔄 Prediction Request Lifecycle

1. Client sends request
2. FastAPI validates input (Pydantic)
3. Data preprocessing pipeline runs
4. Model generates prediction
5. Request + prediction stored in DB
6. Response returned


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
├── 📂 data/                    # datasets
│   ├── Car_details.csv
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


| Metric | Value |
|------|------|
| Training R² | ~96% |
| Testing R²  | ~90% |
| RMSE        | ~0.20 |
| MAE         | ~0.14 |

> Metrics computed on log-transformed target variable


The trained pipeline is saved as:

```
models/latest.joblib
```

---

## 🧾 Model Versioning

* Timestamped models:

  ```
  models/versions/rf_YYYYMMDD.joblib
  ```
* `latest.joblib` → production model
* API always loads latest

✔ Enables:

* reproducibility
* rollback
* experiment tracking

---

# ⚙️ Model Loading Strategy

✔ Model loaded once at startup  
✔ Stored in memory for fast inference  
✔ No per-request loading overhead  

---

## 🧪 Testing

Includes:

* Unit tests (prediction, validation, loader, repository)
* API testing using FastAPI TestClient
* Database testing with isolated test DB
* Integration test (API + MySQL)

Run:

```bash
pytest
pytest --cov=src
```

### ✅ Test Coverage: **89%**

> ✔ Covers API, database, and ML pipeline components

---


## 🧠 Production Considerations

- Non-blocking startup using background model loading
- Database retry mechanism to handle container startup race conditions
- Dependency injection for clean architecture and testability
- Repository pattern for database abstraction
- Environment-based configuration system




## ✅ Input Validation

The system enforces strict validation:

- No missing or extra fields
- Numeric fields must be valid and non-negative
- Categorical fields must match training values

This ensures prediction consistency and prevents silent failures.


## 📊 Logging

- Structured logging for model loading and prediction flow
- Error logging for debugging failures
- Useful for monitoring in production environments


## ⚠️ Limitations

- Model trained on limited dataset
- No real-time model monitoring (model performance is not tracked over time)
- No feature drift detection
- No authentication on API


## 🔄 CI/CD (Planned)

- Automated testing pipeline
- Docker image build & push
- Deployment automation


## 📊 Failure & Tradeoffs

- Linear models underperformed due to non-linear relationships
- RandomForest chosen for better generalization

### Known Weaknesses:
- Sensitive to unseen categorical values
- Performance may degrade with data distribution shifts

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

## 🗄 Database Logging

Every prediction is stored:

**Table: `predictions`**

| Column          | Description  |
| --------------- | ------------ |
| id              | Unique ID    |
| timestamp       | Request time |
| features        | Input JSON   |
| predicted_price | Model output |
| model_version   | Version used |


✔ Enables:

* monitoring
* debugging
* auditing

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
  "prediction": 536241 
}
```

---


## ❌ Error Responses

### Model Not Ready (503)

```json
{
  "detail": "Model is still loading"
}
```

### Validation Error (422)

```json
{
  "detail": [...]
}
```

### Metadata Failure (500)

```json
{
  "detail": "Model Metadata not found"
}
```

---

# 🐳 Docker Deployment

The system is containerized using **Docker**.

---

## Docker Compose 

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


### Why FastAPI?
- High performance
- Built-in validation
- Async support

### Why Docker?
- Reproducible environments
- Simplifies deployment

### Why Pipeline Architecture?
- Separates preprocessing and model logic
- Ensures training/inference consistency


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


This project demonstrates real-world ML challenges:

- Bridging training and inference environments
- Handling model lifecycle and versioning
- Ensuring API reliability under partial system failure
- Maintaining testable and modular backend architecture

These practices reflect how **real-world ML systems are designed, deployed, and maintained in production environments**.

---



# 🚀 Final Note

This is not just a model — it is a **production-ready machine learning system built with real-world engineering principles**.
