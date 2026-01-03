# Vessel Performance – Main Engine Fuel Oil Consumption Prediction

##  Overview

This project predicts **main engine fuel oil consumption** using vessel operational data, propulsion details, and environmental conditions. The model is deployed via **FastAPI** and fully **Dockerized**, making it ready for production use.

##  Problem

The goal is to predict fuel consumption in order to:

* Optimize vessel performance
* Support for Vessel Performance Monitoring
* Reduce fuel costs
* Support informed operational decisions

##  Dataset

* **Source:** FuelCast Dataset
* **Records:** 173,982 (reduced to 21,564 after cleaning)
* **Features:** 93 (final 49 features used)
* **Vessels:** CPS_Poseidon, OSS_Ceto, CPS_Triton

##  Preprocessing

* Target defined as: **ME_Total_MomentaryFuel = Port + Starboard Fuel**
* Removed missing or irrelevant data and duplicates
* Handled outliers using IQR clipping
* Created additional features like rolling mean and standard deviation

##  Model

* **Random Forest:** MAE = 0.00416, R² = 0.966
* **XGBoost (Final Model):** MAE = 0.00507, R² = 0.961
* **Most important features:** Propeller torque and power, engine shaft power, vessel speed

##  FastAPI

* Provides a **REST API** for real-time fuel consumption prediction
* Accepts vessel operational data as input and returns predicted fuel consumption
* Interactive API documentation: [Swagger UI](http://localhost:8001/docs)
* Example endpoint: `/predict`

##  Docker Deployment

```bash
# Pull the Docker image
docker pull viju4912/fuelcast-api:slim

# Run the container
docker run -d -p 8001:8000 --name fuelcast_api viju4912/fuelcast-api:slim
```

##  Architecture

```
[Vessel Sensors & Operational Data]  # Raw data from ship sensors
                ↓
        [Data Preprocessing]  # Cleaning & formatting
                ↓
      [Feature Engineering]  # Rolling stats, derived metrics
                ↓
      [ML Model Pipeline (XGBoost)]  # Predictive model
                ↓
         [FastAPI REST API]  # Exposes prediction endpoint
                ↓
     [Predicted Fuel Consumption]  # Output for decision-making
                ↓
  [Dashboard / Decision Support System]  # Visualization & monitoring
```

## 📈 Outcomes

* Results align well with vessel physics and operational behavior
* Demonstrates expertise in Python, machine learning, XGBoost, FastAPI, and Docker

