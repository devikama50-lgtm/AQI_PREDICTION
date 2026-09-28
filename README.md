# 🌍 Location-Based AQI Prediction

A machine learning project that predicts **Air Quality Index (AQI)** for selected locations using historical environmental data.

## 🛠️ Tech Stack

* Python
* Pandas
* Scikit-learn
* Random Forest Regressor
* FastAPI
* Streamlit
* Joblib

## 📊 Features

The model uses:

* PM2.5
* PM10
* NO₂
* SO₂
* O₃
* CO
* Temperature
* Humidity
* Wind Speed

## ⚙️ How It Works

```text
User selects location
        ↓
Streamlit
        ↓
FastAPI
        ↓
Random Forest Model
        ↓
AQI Prediction
        ↓
Result displayed
```

## 🚀 Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn main:app --reload
```

Start Streamlit in another terminal:

```bash
streamlit run app.py
```

## 📌 Note

The project uses **historical city-level environmental data** and does not provide real-time AQI.

**Built with Python, FastAPI, Machine Learning & Streamlit.**
