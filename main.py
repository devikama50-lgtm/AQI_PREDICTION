from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib

app = FastAPI(title="AQI Prediction API",description="AQI Prediction Based on Location and Environmental Data",version="1.0.0")


model = joblib.load("model.pkl")


city_data = pd.read_csv("city_data.csv", index_col=0)


# Pydantic response model
class AQIResponse(BaseModel):
    city: str
    predicted_aqi: int
    category: str

    pm25: float = Field(description="PM2.5 concentration (µg/m³)")
    pm10: float = Field(description="PM10 concentration (µg/m³)")
    no2: float = Field(description="NO₂ concentration (µg/m³)")
    so2: float = Field(description="SO₂ concentration (µg/m³)")
    o3: float = Field(description="O₃ concentration (µg/m³)")
    co: float = Field(description="CO concentration (mg/m³)")

    temperature: float = Field(description="Temperature (°C)")
    humidity: float = Field(description="Relative humidity (%)")
    wind_speed: float = Field(description="Wind speed (m/s)")


@app.get("/")
def home():
    return {"message": "AQI Prediction API is running","status": "success"}

@app.get("/locations")
def get_locations():
    return {"locations": city_data.index.tolist()}


#determines AQI categorys
def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Moderate"

    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"

    elif aqi <= 200:
        return "Unhealthy"

    elif aqi <= 300:
        return "Very Unhealthy"

    else:
        return "Hazardous"


#Predicts AQI 
@app.get("/predict/{city}", response_model=AQIResponse)
def predict_aqi(city: str):

    
    if city not in city_data.index:
        raise HTTPException(status_code=404,detail="City not found")

    #average environmental values
    data = city_data.loc[city]
    input_data = pd.DataFrame( [data.values], columns=data.index)

    # Prediction
    prediction = model.predict(input_data)[0]

    prediction = round(prediction)

    
    category = get_aqi_category(prediction)

    
    return {
        "city": city,
        "predicted_aqi": prediction,
        "category": category,
        "pm25": round(data["pm25"], 2),
        "pm10": round(data["pm10"], 2),
        "no2": round(data["no2"], 2),
        "so2": round(data["so2"], 2),
        "o3": round(data["o3"], 2),
        "co": round(data["co"], 2),
        "temperature": round(data["temperature"], 2),
        "humidity": round(data["humidity"], 2),
        "wind_speed": round(data["wind_speed"], 2)
    }

@app.get("/model_info")
def model_info():

    return {"model": "Random Forest Regressor","features": 9,"target": "AQI","training_rows": 18000}