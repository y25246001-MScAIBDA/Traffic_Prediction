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
traffic_model = pickle.load(open('Traffic_model.sav', 'rb'))

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
    hour = st.text_input("Hour of the Day (0–23)")
    day = st.text_input("Day of Week (1–7)")

with col2:
    temperature = st.text_input("Temperature (°C)")
    rain = st.text_input("Rain (mm)")

with col3:
    humidity = st.text_input("Humidity (%)")
    wind_speed = st.text_input("Wind Speed")

# -------------------------------
# Prediction
# -------------------------------
traffic_result = ""

if st.button("Predict Traffic"):

    user_input = [
        hour, day, temperature,
        rain, humidity, wind_speed
    ]

    if check_empty_fields(user_input):

        try:
            user_input = [float(x) for x in user_input]

            prediction = traffic_model.predict([user_input])

            # Modify output based on your model
            if prediction[0] == 0:
                traffic_result = "🚗 Low Traffic"
            elif prediction[0] == 1:
                traffic_result = "🚙 Medium Traffic"
            else:
                traffic_result = "🚕 High Traffic"

        except:
            st.error("⚠️ Invalid input format. Please enter numeric values.")

# -------------------------------
# Output
# -------------------------------
st.success(traffic_result)
