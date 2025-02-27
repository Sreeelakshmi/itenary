import streamlit as st
import requests
import os

# OpenWeather API Key (use environment variable or Streamlit secrets)
API_KEY = os.getenv("f8cb952227a9226d7088520604acec5a") 

def get_lat_lon(state_name):
    """Fetch latitude and longitude of a state using OpenWeather Geocoding API."""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={state_name},IN&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return data["lat"], data["lon"]
    else:
        st.error("⚠️ Could not retrieve coordinates. Check the state name.")
        return None, None

def get_weather(state_name):
    """Fetch weather data based on state name."""
    lat, lon = get_lat_lon(state_name)
    if lat is None or lon is None:
        return None

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "Temperature": data["main"]["temp"],
            "Condition": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"]
        }
    else:
        st.error("❌ Failed to retrieve weather data.")
        return None

# Streamlit UI
st.title("Seven Sisters Itinerary Planner 🌍")

state_name = st.selectbox("Select a State", ["Assam", "Meghalaya", "Tripura", "Mizoram", "Manipur", "Nagaland", "Arunachal Pradesh"])

if state_name:
    weather = get_weather(state_name)
    
    if weather:
        st.subheader(f"🌤️ Weather in {state_name}")
        st.write(f"**Temperature:** {weather['Temperature']}°C")
        st.write(f"**Condition:** {weather['Condition'].capitalize()}")
        st.write(f"**Humidity:** {weather['Humidity']}%")
        st.write(f"**Wind Speed:** {weather['Wind Speed']} m/s")
    else:
        st.error("⚠️ Unable to display weather data.")
