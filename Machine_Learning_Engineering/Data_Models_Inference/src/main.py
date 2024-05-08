from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel, ValidationError, field_validator, Extra
import joblib
import numpy as np
import os

app = FastAPI()



model = joblib.load(os.getcwd() + '/trainer/model_pipeline.pkl')
#model = joblib.load('../trainer/model_pipeline.pkl')

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

#Create another Validation model that requires a list of InputModel objects.

class ResponseModel(BaseModel):
	prediction : float


@app.get("/health")
def read_health():
	return {"time": datetime.now().isoformat()}

@app.get("/hello")
def say_hello(name : str):
	if name:
		return {"message": f"Hello {name}"}

@app.post("/predict")
def get_predictions(input_data: InputModel) -> ResponseModel:
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
	
	
	#return prediction.tolist()


