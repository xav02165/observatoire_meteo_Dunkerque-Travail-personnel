from datetime import datetime
import pandas as pd
import requests
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Observatoire Météo - Dunkerque",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⛅ L'Observatoire Météo — Dunkerque")
st.markdown(
    "Tableau de bord de suivi météorologique en temps réel et historique"
    " (FastAPI, SQLite & Streamlit)."
)

API_LIVE_URL = "http://127.0.0.1:8000/weather/live"
API_HISTORY_URL = "http://127.0.0.1:8000/weather/history"


def fetch_data(url):
  try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
      return response.json()
    return None
  except Exception:
    return None


# Barre latérale
with st.sidebar:
  st.header("⚙️ Contrôles")
  if st.button("🔄 Actualiser les données", use_container_width=True):
    st.cache_data.clear()
  st.markdown("---")
  st.markdown("**Localisation :** Dunkerque (51.03N, 2.37E)")
  st.markdown("**Stockage :** Base de données SQLite locale")

# Récupération du temps réel
data = fetch_data(API_LIVE_URL)

if data:
  timestamp_formatted = datetime.fromisoformat(data["timestamp"]).strftime(
      "%d/%m/%Y à %H:%M"
  )
  st.info(f"Dernier relevé horaire synchronisé : **{timestamp_formatted}**")

  # Affichage des KPIs
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.metric(label="🌡️ Température", value=f"{data['temperature']} °C")
  with col2:
    st.metric(label="💨 Vent", value=f"{data['wind_speed']} km/h")
  with col3:
    st.metric(label="💧 Humidité", value=f"{data['humidity']} %")
  with col4:
    st.metric(label="☀️ Indice UV", value=f"{data['uv_index']}")
  with col5:
    pollution = (
        f"{data['air_pollution']}"
        if data.get("air_pollution") is not None
        else "N/A"
    )
    st.metric(label="🌍 Qualité de l'air (AQI)", value=pollution)

else:
  st.error(
      "⚠️ Impossible de joindre l'API FastAPI. Vérifie que ton serveur Uvicorn"
      " est bien actif."
  )

st.markdown("---")

# Section Historique & Graphiques
st.subheader("📈 Historique des Relevés (SQLite)")

history_data = fetch_data(API_HISTORY_URL)

if history_data and len(history_data) > 0:
  df = pd.DataFrame(history_data)
  # Conversion de la colonne timestamp en format date/heure
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  df = df.set_index("timestamp")

  # Onglets pour structurer l'affichage
  tab1, tab2, tab3 = st.tabs(
      ["🌡️ Température", "💨 Vent & Humidité", "📋 Tableau Brut"]
  )

  with tab1:
    st.line_chart(df[["temperature"]])

  with tab2:
    st.line_chart(df[["wind_speed", "humidity"]])

  with tab3:
    st.dataframe(df, use_container_width=True)
else:
  st.info(
      "Aucun historique enregistré pour le moment. Laisse tourner l'application"
      " ou clique sur actualiser pour accumuler des points !"
  )