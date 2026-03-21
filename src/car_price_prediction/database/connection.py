from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from car_price_prediction.config import settings

#? NOTE: The url is set in the config file
# Configure this with the actual database URL before creating the engine.
# URL_DATABASE = 'mysql+pymysql://fastapi_user:password123@db:3306/car_price_db'


# pool_pre_ping prevents dead connections 
# future=True allows to use async functions
engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,      # checks if DB connection is alive
    pool_recycle=3600,       # prevents stale MySQL connections
    future=True
)

#* Session is used to interact with the database.
# autocommit: If True, each statement is automatically given a COMMIT command after execution.
# autoflush: If True, each query will automatically be flushed to the database before returning the result.
# bind: A Connection or Engine to which the Session will be bound.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#* Base class that all ORM models should inherit from.
Base = declarative_base()
