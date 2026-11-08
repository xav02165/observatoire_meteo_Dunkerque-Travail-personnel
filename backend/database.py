from datetime import datetime
import sqlite3

DB_FILE = "backend/weather_observatory.db"


def init_db():
  """Initialise la base de données SQLite et la table des relevés."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT UNIQUE,
            temperature REAL,
            wind_speed REAL,
            humidity REAL,
            uv_index REAL,
            air_pollution REAL
        )
    """)
  conn.commit()
  conn.close()


def save_weather_record(data: dict):
  """Enregistre un relevé météo (ignore si le timestamp existe déjà)."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  try:
    cursor.execute(
        """
            INSERT OR IGNORE INTO weather_records (timestamp, temperature, wind_speed, humidity, uv_index, air_pollution)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("timestamp"),
            data.get("temperature"),
            data.get("wind_speed"),
            data.get("humidity"),
            data.get("uv_index"),
            data.get("air_pollution"),
        ),
    )
    conn.commit()
  except Exception as e:
    print(f"Erreur SQLite : {e}")
  finally:
    conn.close()


def get_history_data():
  """Récupère l'historique complet trié par date."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        SELECT timestamp, temperature, wind_speed, humidity, uv_index, air_pollution 
        FROM weather_records 
        ORDER BY timestamp ASC
    """)
  rows = cursor.fetchall()
  conn.close()
  return rows