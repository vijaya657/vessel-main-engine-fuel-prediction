from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# ===============================
# Load trained pipeline
# ===============================
model = joblib.load("me_fuel_xgb_pipeline.pkl")

# ===============================
# FastAPI app
# ===============================
app = FastAPI(
    title="Main Engine Fuel Consumption Prediction API",
    description="Predicts total main engine momentary fuel consumption",
    version="1.0"
)

# ===============================
# Allowed vessels (STRICT)
# ===============================
ALLOWED_VESSELS = [
    "CPS_Triton",
    "CPS_Poseidon",
    "CPS_Apollo"
]

# ===============================
# Input schema (WITH vessel_name)
# ===============================
class FuelInput(BaseModel):

    # 🔹 Vessel (categorical)
    vessel_name: str

    # 🔹 Main Engine
    Consumer_MainEnginePort_RotationSpeed: float
    Consumer_MainEnginePort_ShaftPower: float
    Consumer_MainEngineStarboard_RotationSpeed: float
    Consumer_MainEngineStarboard_ShaftPower: float

    # 🔹 Environment
    Environment_SeaFloorDepth: float

    # 🔹 Propeller
    Propeller_Port_RotationSpeed: float
    Propeller_Port_ShaftPower: float
    Propeller_Port_ShaftTorque: float
    Propeller_Starboard_RotationSpeed: float
    Propeller_Starboard_ShaftPower: float
    Propeller_Starboard_ShaftTorque: float
    Propeller_Total_ShaftPower: float

    # 🔹 Ship
    Ship_AirTemperature: float
    Ship_AnemometerWindDirection: float
    Ship_AnemometerWindSpeed: float
    Ship_Bearing: float
    Ship_DraftAft: float
    Ship_DraftFore: float
    Ship_Heading: float
    Ship_SpeedOverGround: float
    Ship_SpeedThroughWater: float

    # 🔹 Weather
    Weather_DiffuseRadiation: float
    Weather_DirectNormalIrradiance: float
    Weather_DirectRadiation: float
    Weather_OceanCurrentDirection: float
    Weather_OceanCurrentVelocity: float
    Weather_Precipitation: float
    Weather_RelativeHumidity2M: float
    Weather_ShortwaveRadiation: float
    Weather_SunshineDuration: float
    Weather_SurfacePressure: float
    Weather_SwellWaveDirection: float
    Weather_SwellWaveHeight: float
    Weather_SwellWavePeakPeriod: float
    Weather_SwellWavePeriod: float
    Weather_Temperature2M: float
    Weather_WaveDirection: float
    Weather_WaveHeight: float
    Weather_WavePeriod: float
    Weather_WeatherCode: float
    Weather_WindDirection10M: float
    Weather_WindGusts10M: float
    Weather_WindSpeed10M: float
    Weather_WindWaveDirection: float
    Weather_WindWaveHeight: float
    Weather_WindWavePeakPeriod: float
    Weather_WindWavePeriod: float

    # 🔹 Fuel rolling stats
    Fuel_roll_mean_5: float
    Fuel_roll_std_5: float


# ===============================
# Health check
# ===============================
@app.get("/")
def home():
    return {"status": "API is running"}

# ===============================
# Prediction endpoint
# ===============================
@app.post("/predict")
def predict_fuel(data: FuelInput):

    # ✅ Vessel validation
    if data.vessel_name not in ALLOWED_VESSELS:
        return {
            "error": "Invalid vessel_name",
            "allowed_vessels": ALLOWED_VESSELS
        }

    # ✅ Convert input to DataFrame
    df = pd.DataFrame([data.dict()])

    # ✅ Predict
    prediction = model.predict(df)[0]

    return {
        "vessel_name": data.vessel_name,
        "predicted_ME_Total_MomentaryFuel": round(float(prediction), 6)
    }
