from .database import get_history_data, init_db, save_weather_record
from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI(
    title="L'Observatoire Météo API",
    version="1.0.0",
)


# Initialisation de la base de données au lancement de l'API
@app.on_event("startup")
def startup_event():
  init_db()


class WeatherRecord(BaseModel):
  timestamp: str
  temperature: float
  wind_speed: float
  humidity: float
  uv_index: float
  air_pollution: float | None = None


@app.get("/weather/live", response_model=WeatherRecord)
def get_live_weather():
  LAT, LON = 51.0343, 2.3767  # Coordonnées de Dunkerque
  url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
  air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={LAT}&longitude={LON}&current=european_aqi"

  try:
    response = requests.get(url, timeout=10)
    weather_data = response.json()

    air_response = requests.get(air_url, timeout=10)
    air_data = air_response.json()

    current_w = weather_data.get("current", {})
    current_a = air_data.get("current", {})

    record = {
        "timestamp": current_w.get("time"),
        "temperature": current_w.get("temperature_2m"),
        "wind_speed": current_w.get("wind_speed_10m"),
        "humidity": current_w.get("relative_humidity_2m"),
        "uv_index": 0.0,  # Valeur par défaut si non récupérée
        "air_pollution": current_a.get("european_aqi"),
    }

    # Sauvegarde automatique dans SQLite à chaque consultation en direct
    save_weather_record(record)

    return record
  except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Erreur lors de la récupération des données : {str(e)}",
    )


@app.get("/weather/history")
def get_weather_history():
  """Renvoie l'historique stocké dans la base SQLite."""
  rows = get_history_data()
  history = []
  for row in rows:
    history.append({
        "timestamp": row[0],
        "temperature": row[1],
        "wind_speed": row[2],
        "humidity": row[3],
        "uv_index": row[4],
        "air_pollution": row[5],
    })
  return history