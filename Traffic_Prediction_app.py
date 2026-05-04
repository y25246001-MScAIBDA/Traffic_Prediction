# -*- coding: utf-8 -*-
"""
Smart Traffic Prediction System - Advanced Streamlit Dashboard
"""

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import datetime

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Smart Traffic Prediction System",
    layout="wide",
    page_icon="🚦"
)

# -------------------------------
# Load Model
# -------------------------------
model = pickle.load(open("traffic_model.sav", "rb"))
encoder = pickle.load(open("weather_encoder.sav", "rb"))

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🚦 Smart Traffic")
menu = st.sidebar.radio("Navigation", ["Home", "Predict Traffic", "About"])

# -------------------------------
# HOME PAGE
# -------------------------------
if menu == "Home":

    st.title("🚦 Smart Traffic Prediction System")
    st.markdown("Real-time traffic insights and machine learning predictions")

    col1, col2, col3, col4 = st.columns(4)

    # Fake dynamic data (for dashboard look)
    col1.metric("Current Traffic", "LOW", "↓")
    col2.metric("Avg Traffic Score", "2.3 / 5")
    col3.metric("Vehicles on Road", "2,814", "+120")
    col4.metric("Peak Hour", "5 PM - 7 PM")

    st.markdown("---")

    # Traffic Trend Chart
    st.subheader("📈 Traffic Trend (Today)")

    hours = list(range(24))
    traffic_values = [np.sin(h/3)+2 for h in hours]

    df = pd.DataFrame({
        "Hour": hours,
        "Traffic": traffic_values
    })

    st.line_chart(df.set_index("Hour"))

    # Pie Chart
    st.subheader("📊 Traffic Distribution")

    pie_data = pd.DataFrame({
        "Zone": ["Zone A", "Zone B", "Zone C"],
        "Traffic": [38, 36, 26]
    })

    st.bar_chart(pie_data.set_index("Zone"))

    st.success("✅ System running successfully")

# -------------------------------
# PREDICTION PAGE
# -------------------------------
elif menu == "Predict Traffic":

    st.title("🚦 Predict Traffic")

    col1, col2 = st.columns(2)

    # Inputs
    with col1:
        day = st.selectbox("Day",
                           ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

        hour = st.slider("Hour", 0, 23, 12)

        weather = st.selectbox("Weather",
                               ["Clear","Clouds","Rain","Snow","Mist","Fog"])

    with col2:
        temperature = st.slider("Temperature (°C)", -10, 50, 25)
        rain = st.slider("Rain (mm)", 0.0, 20.0, 0.0)
        snow = st.slider("Snow (mm)", 0.0, 20.0, 0.0)
        holiday = st.selectbox("Holiday", ["No","Yes"])

    # Encoding
    day_map = {
        "Monday":0,"Tuesday":1,"Wednesday":2,
        "Thursday":3,"Friday":4,"Saturday":5,"Sunday":6
    }

    day_encoded = day_map[day]
    holiday_encoded = 1 if holiday == "Yes" else 0
    weather_encoded = encoder.transform([weather])[0]

    # Prediction
    if st.button("🚦 Predict Traffic"):

        input_data = [[
            hour,
            day_encoded,
            holiday_encoded,
            temperature,
            rain,
            snow,
            weather_encoded
        ]]

        prediction = model.predict(input_data)[0]

        if prediction == 0:
            st.success("🚗 Low Traffic")
        elif prediction == 1:
            st.warning("🚙 Medium Traffic")
        else:
            st.error("🚕 High Traffic")

# -------------------------------
# ABOUT PAGE
# -------------------------------
else:

    st.title("📘 About System")

    st.markdown("""
### 🚦 Smart Traffic Prediction System

This project uses Machine Learning to predict traffic conditions based on:

- Time (Hour, Day)
- Weather conditions
- Temperature
- Rain and Snow
- Holiday data

### ⚙️ Model Used:
- Random Forest Classifier

### 🎯 Output:
- Low Traffic
- Medium Traffic
- High Traffic

### 🚀 Built With:
- Python
- Streamlit
- Scikit-learn
""")
