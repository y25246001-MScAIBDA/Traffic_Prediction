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
Traffic_model = pickle.load(open('Traffic_model.sav', 'rb'))

# -------------------------------
# Validation Function
# -------------------------------
def check_empty_fields(input_list):
    for value in input_list:
        if str(value).strip() == "":
            st.error("⚠️ Please fill all input values.")
            return False
    return True

# -------------------------------
# Title
# -------------------------------
st.title("🚦 Traffic Prediction using Machine Learning")

st.write("Enter the details below to predict traffic conditions.")

# -------------------------------
# Input Fields (EDIT based on your model features)
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    coded_day = st.number_input("Coded Day (0–6)", min_value=0, max_value=6)
    zone = st.number_input("Zone (numeric encoded)")

with col2:
    weather = st.number_input("Weather (encoded)")
    temperature = st.number_input("Temperature (°C)")
# -------------------------------
# Prediction
# -------------------------------
traffic_result = ""

if st.button("Predict Traffic"):

    user_input = [
        coded_day,
        zone,
        weather,
        temperature
    ]

    try:
        prediction = Traffic_model.predict([user_input])[0]

        # 🔥 Convert numeric output to traffic level
        if prediction < 2:
            result = "🚗 Low Traffic"
        elif prediction < 4:
            result = "🚙 Medium Traffic"
        else:
            result = "🚕 High Traffic"

        st.success(f"Traffic Prediction: {result}")
        st.info(f"Raw Value: {round(prediction, 2)}")

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------------
# Output
# -------------------------------
st.success(traffic_result)
