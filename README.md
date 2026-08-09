# 🌱 Smart Urban Gardening Advisory System Using IoT Technology

A responsive web application that helps urban gardeners manage their plants,
detect leaf diseases using machine learning, receive weather-aware care
recommendations, monitor simulated IoT sensor data, get automatic alerts,
and connect with local plant nurseries — all in one place.

Built with **Python (Flask)**, **Bootstrap 5**, **SQLite**, and a
**TensorFlow/Keras MobileNetV2** deep learning model, fine-tuned via
transfer learning on a labeled dataset of leaf diseases.

---

## 👥 Team

| Name | Role / Modules |
|---|---|
| *(add name)* | Authentication, Plant Management, Disease Detection |
| *(add name)* | Weather Recommendation, IoT Sensor Module, Alert Module |
| *(add name)* | Nursery Module, Knowledge Base |

---

## ✨ Features

| # | Module | What it does |
|---|---|---|
| 1 | **Authentication** | Register / log in as a Gardener or Nursery Owner, session-based login, bcrypt password hashing |
| 2 | **Plant Management** | Add, view, edit, and delete plants in a personal garden dashboard |
| 3 | **Disease Detection** | Upload a leaf photo, get an AI-predicted disease label with a confidence score and a treatment recommendation, with full diagnosis history |
| 4 | **Weather Recommendation** | Live current weather + 5-day forecast (OpenWeatherMap), plus a weather-aware watering recommendation |
| 5 | **IoT Sensor Module** | Pair a (simulated) sensor to a plant and generate realistic soil moisture / temperature / humidity readings over time |
| 6 | **Alert Module** | Configurable soil-moisture thresholds trigger automatic alerts; disease detections also raise alerts; unread-count badge in the navbar |
| 7 | **Nursery Module** | Nursery Owners list tools/plants/fertilizer for sale; Gardeners browse and search the shared marketplace |
| 8 | **Knowledge Base** | Searchable library of plant care and disease-treatment articles |

---

## 🧠 Machine Learning

Disease Detection is powered by **MobileNetV2** (pretrained on ImageNet),
fine-tuned via **transfer learning** on a real leaf-disease dataset covering
6 vegetables and 21 disease/healthy classes. Training was done in Google
Colab; the trained model achieved **97%+ validation accuracy**.

- `ml_model/plant_model.keras` — the trained model
- `ml_model/labels.json` — the ordered class list the model predicts

> If these two files are not present, the app automatically falls back to
> clearly-labeled **mock predictions** so every other feature remains fully
> testable without a trained model.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask (Blueprints architecture) |
| Database | SQLite + SQLAlchemy ORM |
| Frontend | Bootstrap 5, Jinja2 templates, minimal vanilla JavaScript |
| Machine Learning | TensorFlow / Keras, MobileNetV2 (transfer learning) |
| Auth & Security | Flask-Login (sessions), Flask-Bcrypt (password hashing) |
| External API | OpenWeatherMap (current weather + 5-day forecast) |
| Config | python-dotenv (`.env` file) |

---

## 📁 Project Structure

```
smart_garden/
├── app.py                    # Application factory + entry point
├── config.py                  # Settings (env-var overridable)
├── extensions.py              # Shared db / bcrypt / login_manager instances
├── requirements.txt
├── .env.example                # Copy to .env and fill in your own values
├── models/                    # SQLAlchemy ORM models (one file per entity)
├── blueprints/                 # One Flask Blueprint per module
│   ├── auth/                    # Module 1
│   ├── plants/                   # Module 2
│   ├── disease/                   # Module 3
│   ├── weather/                    # Module 4
│   ├── sensors/                     # Module 5
│   ├── alerts/                       # Module 6
│   ├── nursery/                       # Module 7
│   └── knowledge_base/                 # Module 8
├── templates/                   # Jinja2 HTML templates (Bootstrap 5)
├── static/                       # CSS and JavaScript
├── utils/                         # Validators, access control, ML predictor,
│                                     weather service, rule engines, etc.
├── uploads/                     # Uploaded leaf images (created at runtime)
└── ml_model/                    # Trained model files go here
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> `tensorflow-cpu` is a large package — this step can take a few minutes.

### 4. Configure environment variables

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

| Variable | Required? | Purpose |
|---|---|---|
| `OPENWEATHER_API_KEY` | Optional | Enables real weather data (Module 4). Get a free key at [openweathermap.org/api](https://openweathermap.org/api). Without it, the app shows clearly-labeled placeholder forecasts. |
| `SECRET_KEY` | Recommended | Flask session signing key — change from the default before any real deployment. |
| `DEFAULT_WEATHER_LOCATION` | Optional | Default city for weather lookups (defaults to `Dhaka,BD`). |

### 5. (Optional) Add the trained ML model

Place `plant_model.keras` and `labels.json` into the `ml_model/` folder. Without
them, Disease Detection runs in mock-prediction mode automatically.

### 6. Run the application

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 🧪 Testing

Register two accounts to explore both roles:
- A **Gardener** account — access Plant Management, Disease Detection, Weather,
  Sensors, Alerts, Knowledge Base, and Marketplace browsing
- A **Nursery Owner** account — access product listing management

---

## 📊 Database Schema

10 SQLAlchemy models, one per entity: `User`, `Plant`, `Sensor`,
`SensorReading`, `DiagnosisResult`, `ThresholdSetting`, `Alert`,
`WeatherForecast`, `CareRecommendation`, `NurseryProduct`,
`KnowledgeBaseArticle`.

---

## 🔒 Security Notes

- Passwords are hashed with **bcrypt** (never stored in plain text)
- **Ownership-based access control**: users can only view/edit their own
  plants, products, and alerts — enforced on every route
- All state-changing actions (delete, simulate, acknowledge) are **POST-only**
- Secrets are loaded from a local `.env` file, excluded from version control

---

## 📚 Dataset Acknowledgment

The disease detection model was trained on a plant leaf freshness and
disease dataset covering Bitter Gourd, Bottle Gourd, Cauliflower, Cucumber,
Eggplant, and Tomato.

---

## 📄 License

This project was developed for academic purposes as part of a Software
Engineering course project.
