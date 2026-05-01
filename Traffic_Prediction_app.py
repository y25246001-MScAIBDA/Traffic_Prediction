# -*- coding: utf-8 -*-
"""
Traffic Prediction Streamlit App (Final - Correct Version)
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
# Load Model + Encoder
# -------------------------------

import gdown

url = "https://drive.google.com/file/d/1zQVWOdWW-jyx_F3LSkvcEn8FBZvhSi8F/view?usp=sharing"
output = "traffic_model.sav"

gdown.download(url, output, quiet=False)


traffic_model = pickle.load(open('traffic_model.sav', 'rb'))
weather_encoder = pickle.load(open('weather_encoder.sav', 'rb'))

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
    day = st.selectbox(
        "Select Day",
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    )

# Hour selection (IMPORTANT 🔥)
with col2:
    hour = st.slider("Select Hour (0–23)", 0, 23, 12)

# Weather selection
with col1:
    weather = st.selectbox(
        "Weather Condition",
        ["Clear","Clouds","Rain","Snow","Mist","Fog"]
    )

# Temperature
with col2:
    temperature = st.slider("Temperature (°C)", -10, 50, 25)

# Rain & Snow
with col1:
    rain = st.slider("Rain (mm)", 0.0, 20.0, 0.0)

with col2:
    snow = st.slider("Snow (mm)", 0.0, 20.0, 0.0)

# Holiday
is_holiday = st.selectbox("Is Holiday?", ["No", "Yes"])

# -------------------------------
# Encoding
# -------------------------------

# Day encoding
day_map = {
    "Monday":0, "Tuesday":1, "Wednesday":2,
    "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6
}

day_encoded = day_map[day]

# Holiday encoding
holiday_encoded = 1 if is_holiday == "Yes" else 0

# Weather encoding (from trained encoder)
try:
    weather_encoded = weather_encoder.transform([weather])[0]
except:
    st.error("⚠️ Weather value not recognized by model.")
    weather_encoded = 0

# -------------------------------
# Prediction
# -------------------------------
if st.button("🚦 Predict Traffic"):

    try:
        # IMPORTANT: Must match training features EXACTLY
        user_input = [
            hour,
            day_encoded,
            holiday_encoded,
            temperature,
            rain,
            snow,
            weather_encoded
        ]

        prediction = traffic_model.predict([user_input])[0]

        # Convert to readable result
        if prediction == 0:
            result = "🚗 Low Traffic"
        elif prediction == 1:
            result = "🚙 Medium Traffic"
        else:
            result = "🚕 High Traffic"

        # Output
        st.success(result)

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------------
# Info Section
# -------------------------------
st.markdown("""
---
### ℹ️ About Model
This model predicts traffic using:

- Hour of the day ⏰  
- Day of week 📅  
- Holiday 🎉  
- Weather 🌦️  
- Temperature 🌡️  
- Rain & Snow 🌧️  

Model: RandomForestClassifier  
Output: Low / Medium / High Traffic
""")
