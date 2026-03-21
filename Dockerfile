FROM python:3.11-slim

# create and change to the app directory
WORKDIR /app

# copy the dependencies file to the working directory
COPY pyproject.toml /app

# copy the content of the local src directory to the working directory
COPY src /app/src

# install dependencies
RUN pip install --no-cache-dir .


# copy the content of the local models directory to the working directory
COPY models /app/models
# copy the content of the local reports directory to the working directory
COPY reports /app/reports


# expose means that this port will be available to the outside world
EXPOSE 10000


# command to run on container start
CMD ["uvicorn", "car_price_prediction.api:app", "--host", "0.0.0.0", "--port", "10000"]