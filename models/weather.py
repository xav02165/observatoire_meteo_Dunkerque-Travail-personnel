from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WeatherRecord(BaseModel):
    """Modèle Pydantic pour la validation des données météo horaires."""
    
    timestamp: datetime = Field(..., description="Date et heure de l'enregistrement")
    temperature: float = Field(..., description="Température en °C", ge=-50.0, le=60.0)
    wind_speed: float = Field(..., description="Vitesse du vent en km/h", ge=0.0)
    humidity: int = Field(..., description="Hygrométrie en %", ge=0, le=100)
    uv_index: float = Field(..., description="Indice UV", ge=0.0)
    air_pollution: Optional[float] = Field(None, description="Indice de pollution de l'air (ex: PM2.5 ou AQI)")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "timestamp": "2026-06-06T12:00:00",
                "temperature": 21.5,
                "wind_speed": 14.2,
                "humidity": 65,
                "uv_index": 5.2,
                "air_pollution": 12.4
            }
        }