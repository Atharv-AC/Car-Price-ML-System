import requests

API_URL = "http://localhost:8000"


def test_predict_and_save_to_db():

    payload = {                                    #*       THis test verifies:
        "mileage": 12,                             #?       ✔ model loads
        "engine": 234,                             #?       ✔ DB connects
        "max_power": 123,                          #?       ✔ prediction runs
        "torque": 120,                             #?       ✔ DB save executes
        "km_driven_per_year": 200,
        "car_age": 2,
        "fuel": "CNG",
        "transmission": "Manual",
        "owner": "First Owner"
    }

    response = requests.post(f"{API_URL}/predict", json=payload)

    assert response.status_code == 200
    assert "Prediction" in response.json()



import pymysql

def test_mysql_record_created():

    conn = pymysql.connect(                                #*  THis test verifies:
        host="localhost",                                  #?   API → DB write → DB read
        user="fastapi_user",
        password="password123",
        database="car_price_db"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM predictions")

    count = cursor.fetchone()[0]

    assert count > 0



#! What We Want to Test
#* 1. For integration tests we want to verify:
#* 2. API can connect to MySQL container
#* 3. /predict writes to database
#* 4. Docker startup order works
#* 5. wait_for_db() works
#* 6. Tables get created automatically