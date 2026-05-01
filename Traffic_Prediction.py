# -*- coding: utf-8 -*-
"""
Created on Fri May  1 14:30:26 2026

@author: asusl
"""

# -*- coding: utf-8 -*-
"""
Traffic Prediction App 
"""

import pickle
import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Traffic Prediction System",
    layout="wide",
    page_icon="🚦"
)

# -------------------------------
# Load Model
# -------------------------------
traffic_model = pickle.load(open('traffic_model.sav', 'rb'))

# -------------------------------
# Title
# -------------------------------
st.title("🚦 Traffic Prediction using Machine Learning")
st.markdown("### Enter details to predict traffic conditions")

# -------------------------------
# Input Section
# -------------------------------
st.subheader("📊 Traffic Inputs")

col1, col2 = st.columns(2)

# Day selection
with col1:
    day = st.selectbox("Select Day", 
                       ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

# Zone selection
with col2:
    zone = st.selectbox("Select Zone", 
                        ["Zone A","Zone B","Zone C"])

# Weather selection
with col1:
    weather = st.selectbox("Weather Condition", 
                           ["Clear","Rain","Snow"])

# Temperature
with col2:
    temperature = st.slider("Temperature (°C)", -10, 50, 25)

# -------------------------------
# Encoding (VERY IMPORTANT)
# -------------------------------

day_map = {
    "Monday":0, "Tuesday":1, "Wednesday":2,
    "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6
}

zone_map = {
    "Zone A":0, "Zone B":1, "Zone C":2
}

weather_map = {
    "Clear":0, "Rain":1, "Snow":2
}

coded_day = day_map[day]
zone = zone_map[zone]
weather = weather_map[weather]

# -------------------------------
# Prediction
# -------------------------------
if st.button("🚦 Predict Traffic"):

    try:
        user_input = [
            coded_day,
            zone,
            weather,
            temperature
        ]

        prediction = traffic_model.predict([user_input])[0]

        # Convert numeric output → category
        if prediction < 2:
            result = "🚗 Low Traffic"
        elif prediction < 4:
            result = "🚙 Medium Traffic"
        else:
            result = "🚕 High Traffic"

        # Output
        st.success(f"{result}")
        st.info(f"Prediction Value: {round(prediction,2)}")

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------------
# Info Section
# -------------------------------
st.markdown("""
---
### ℹ️ About Model
This ML model predicts traffic based on:
- Day of the week  
- Zone  
- Weather condition  
- Temperature  

Built using Support Vector Regression (SVR)
""")
