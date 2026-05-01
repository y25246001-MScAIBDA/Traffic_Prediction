# -*- coding: utf-8 -*-
"""
Created on Fri May  1 14:30:26 2026

@author: asusl
"""

# -*- coding: utf-8 -*-
"""
Traffic Prediction Streamlit App
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
col1, col2, col3 = st.columns(3)

with col1:
    hour = st.number_input("Hour of the Day (0–23)", min_value=0, max_value=23, step=1)
    day = st.number_input("Day of Week (1–7)", min_value=1, max_value=7, step=1)

with col2:
    temperature = st.number_input("Temperature (°C)")
    rain = st.number_input("Rain (mm)")

with col3:
    humidity = st.number_input("Humidity (%)")
    wind_speed = st.number_input("Wind Speed")

# -------------------------------
# Prediction
# -------------------------------
traffic_result = ""

if st.button("Predict Traffic"):

    user_input = [
        hour, day, temperature,
        rain, humidity, wind_speed
    ]

    try:
        prediction = traffic_model.predict([user_input])

        if prediction[0] == 0:
            st.success("🚗 Low Traffic")
        elif prediction[0] == 1:
            st.success("🚙 Medium Traffic")
        else:
            st.success("🚕 High Traffic")

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------------
# Output
# -------------------------------
st.success(traffic_result)
