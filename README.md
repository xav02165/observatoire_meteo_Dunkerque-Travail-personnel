# ⛅ L'Observatoire Météo — Dunkerque

Tableau de bord de suivi météorologique horaire en temps réel et historique pour la ville de Dunkerque. L'application combine une architecture **FastAPI** robuste pour le backend, une base de données **SQLite** pour la persistance des données, et une interface interactive **Streamlit** pour la visualisation des indicateurs et graphiques d'évolution.

---

## 🏗️ Architecture du Projet

Le projet est structuré de manière modulaire afin de séparer la logique de l'API backend, la persistance des données et l'interface utilisateur frontend :

```text
observatoire_meteo/
├── backend/
│   ├── main.py                # Application FastAPI (endpoints /weather/live et /weather/history)
│   ├── database.py            # Gestion de la base SQLite (initialisation & requêtes)
│   └── weather_observatory.db # Fichier SQLite persistant (généré automatiquement)
├── frontend/
│   └── app.py                 # Dashboard Streamlit (KPIs, graphiques Pandas & tableaux)
├── run.py                     # Script d'entrée principal pour démarrer Uvicorn
└── requirements.txt           # Dépendances Python nécessaires au projet
```

---

## 🛠️ Stack Technique & Composants

- **Backend :** FastAPI, Uvicorn, Pydantic (validation automatique et typage strict des données météo).
- **Base de données :** SQLite (stockage local persistant des relevés horaires).
- **Frontend :** Streamlit, Pandas (visualisation temps réel et graphiques d'évolution).
- **Source de données :** API Open-Meteo (relevés météo actuels et indice de qualité de l'air).
- **Environnement :** Python 3.14 fonctionnant dans un environnement virtuel dédié (`venv`).

---

## 📍 Localisation et Métriques Suivies

L'observatoire suit en continu la station météorologique géolocalisée à **Dunkerque (51.0343° N, 2.3767° E)**.

Les métriques synchronisées comprennent :
1. **Température (°C)** — Température de l'air à 2 mètres du sol.
2. **Vitesse du vent (km/h)** — Vitesse du vent mesurée à 10 mètres.
3. **Humidité relative (%)** — Pourcentage d'humidité dans l'air.
4. **Indice UV** — Niveau de rayonnement ultraviolet.
5. **Qualité de l'air (AQI European)** — Indice officiel européen de qualité de l'air.

---

## 📋 Prérequis

- **Python** (version 3.14 recommandée) installé sur votre système.
- Un terminal d'exécutions (PowerShell sous Windows ou Bash/Zsh sous Linux/macOS).

---

## 🚀 Guide d'Installation

### 1. Ouvrir le terminal dans le projet
Placez-vous dans le dossier racine de l'application :
```powershell
cd C:\Users\xavdx\Desktop\observatoire_meteo
```

### 2. Créer et activer l'environnement virtuel (`venv`)
Créez un environnement virtuel isolé :
```powershell
python -m venv venv
```

Activez l'environnement virtuel :
- **Sous Windows (PowerShell) :**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Sous Linux / macOS :**
  ```bash
  source venv/bin/activate
  ```

### 3. Installer les dépendances
Installez l'ensemble des modules requis spécifiés dans `requirements.txt` :
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## ▶️ Guide d'Exécution

Pour faire fonctionner l'ensemble de l'observatoire, vous devez exécuter le **Backend (FastAPI)** et le **Frontend (Streamlit)** en parallèle dans deux terminaux distincts.

### Terminal 1 : Démarrage du Backend (FastAPI)
Exécutez le script d'entrée principal :
```powershell
.\venv\Scripts\python run.py
```
- **API Backend :** `http://127.0.0.1:8000`
- **Documentation Swagger UI :** `http://127.0.0.1:8000/docs`

### Terminal 2 : Démarrage du Frontend (Streamlit)
Dans une seconde fenêtre de terminal, activez le `venv` et lancez l'application Streamlit :
```powershell
.\venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```
- **Dashboard Web :** Se lance automatiquement sur `http://localhost:8501`.

---

## 🔌 Documentation des Endpoints FastAPI

- **`GET /weather/live`**
  - Interroge l'API externe Open-Meteo pour les coordonnées de Dunkerque.
  - Valide les données collectées à l'aide de modèles Pydantic.
  - Enregistre automatiquement le relevé horodaté dans la base SQLite (`backend/weather_observatory.db`).
  - Renvoie le JSON du relevé en temps réel.

- **`GET /weather/history`**
  - Extrait l'ensemble des enregistrements historisés depuis la table SQLite `weather_records`.
  - Renvoie une liste chronologique complète de données exploitables par Pandas et Streamlit.

---

## 💾 Fonctionnement & Persistance de la Base SQLite

- La base de données est stockée localement dans **`backend/weather_observatory.db`**.
- **Création automatique :** Le fichier `.db` et sa table `weather_records` sont générés automatiquement au tout premier lancement du backend FastAPI.
- **Persistance :** Les données enregistrées ne sont pas perdues lorsque vous coupez les terminaux ou éteignez la machine. À chaque nouveau lancement, l'historique précédent reste disponible et continue de s'enrichir au fil des rafraîchissements.