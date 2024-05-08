import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from joblib import load
from redis import asyncio

from datetime import datetime
from pydantic import BaseModel, ValidationError, field_validator, Extra
from typing import List
import os
import numpy as np

from fastapi_cache.decorator import cache

# Lab 4 Source Code

class InputModel(BaseModel, extra='forbid'):
	MedInc : float
	HouseAge : float
	AveRooms : float
	AveBedrms : float
	Population : float
	AveOccup : float
	Latitude : float
	Longitude : float

	@field_validator('Latitude')
	def validate_latitude(cls, v: float):
		#Latitude must be between -90 and 90 degrees inclusive.
		if (v < -90 or v > 90):
			raise ValueError("Invalid value for Latitude")
		return v
	
	@field_validator('Longitude')
	def validate_longitude(cls, v: float):
		#Longitude must be between -180 and 180 degrees inclusive	
		if (v < -180 or v > 180):
			raise ValueError("Invalid value for Longitude")
		return v
	
	def to_np_array(self):
		return np.array([self.MedInc, self.HouseAge, self.AveRooms, 
		self.AveBedrms, self.Population, self.AveOccup, self.Latitude, self.Longitude])

class BatchInputModel(BaseModel):
	houses: List[InputModel]


class ResponseModel(BaseModel):
	prediction : float

class BatchResponseModel(BaseModel):
	predictions: List[float]


logger = logging.getLogger(__name__)


LOCAL_REDIS_URL = "redis://localhost:6379/0"


@asynccontextmanager
async def lifespan_mechanism(app: FastAPI):
    logging.info("Starting up Lab4 API")

    # Load the Model on Startup
    global model
    model = load('model_pipeline.pkl')

    # Load the Redis Cache
    if "REDIS_URL" in os.environ:
        HOST_URL = os.getenv("REDIS_URL")  # replace this according to the Lab Requirements
    else:
        HOST_URL = LOCAL_REDIS_URL


	
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)

    # We initialize the connection to Redis and declare that all keys in the
    # database will be prefixed with w255-cache-predict. Do not change this
    # prefix for the submission.
    FastAPICache.init(RedisBackend(redis), prefix="w255-cache-prediction")

    yield
    # We don't need a shutdown event for our system, but we could put something
    # here after the yield to deal with things during shutdown
    logging.info("Shutting down Lab3 API")


app = FastAPI(lifespan=lifespan_mechanism)


# Do not change this function name.
# See the Input Vectorization subsection in the readme for more instructions
@app.post("/bulk-predict")
@cache()
async def multi_predict(data: BatchInputModel) -> BatchResponseModel:
	prediction_outputs = model.predict(np.vstack(list(map(InputModel.to_np_array, data.houses))))
	return BatchResponseModel(predictions = prediction_outputs.tolist())
    

@app.get("/health")
def read_health():
	return {"time": datetime.now().isoformat()}

@app.get("/hello")
def say_hello(name : str):
	if name:
		return {"message": f"Hello {name}"}

@app.post("/predict")
@cache()
async def get_predictions(input_data: InputModel) -> ResponseModel:
	medinc = input_data.MedInc
	houseAge = input_data.HouseAge
	aveRooms = input_data.AveRooms
	aveBedrms = input_data.AveBedrms
	population = input_data.Population
	aveOccup = input_data.AveOccup
	latitude = input_data.Latitude
	longitude = input_data.Longitude

	values = np.array([medinc, houseAge, aveRooms, aveBedrms, population, aveOccup, latitude, longitude])

	prediction = model.predict(values.reshape(1,-1))


	return ResponseModel(prediction=prediction[0])




#def get_bulk_predictions(input_data: BatchInputModel) -> BatchResponseModel:

	







