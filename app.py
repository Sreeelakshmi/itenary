import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt
from io import BytesIO

# OpenWeatherMap API Key (Replace with your own API key)
API_KEY = "f8cb952227a9226d7088520604acec5a"

# Define Seven Sister Cities with their lat/lon
cities = {
    "Guwahati, Assam": (26.1445, 91.7362),
    "Shillong, Meghalaya": (25.5788, 91.8933),
    "Cherrapunji, Meghalaya": (25.2841, 91.7211),
    "Kohima, Nagaland": (25.6747, 94.1100),
    "Imphal, Manipur": (24.8170, 93.9368),
    "Aizawl, Mizoram": (23.7367, 92.7146),
    "Agartala, Tripura": (23.8315, 91.2868),
    "Itanagar, Arunachal Pradesh": (27.0844, 93.6053)
}

# Function to fetch weather data
def get_weather(city, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"]
        }
    return None

# Streamlit UI
st.title("🌏 Seven Sisters Travel Itinerary Planner")
st.sidebar.header("Trip Customization")
travel_date = st.sidebar.date_input("Select your travel date", datetime.date.today())

st.write(f"## 🗓️ Travel Date: {travel_date}")
st.write("This itinerary adapts to real-time weather conditions in the Seven Sister States of India.")

for city, (lat, lon) in cities.items():
    weather = get_weather(city, lat, lon)
    if weather:
        st.subheader(f"📍 {city}")
        col1, col2 = st.columns([1, 3])
        with col1:
            icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
            st.image(icon_url, width=80)
        with col2:
            st.write(f"🌡️ **Temperature:** {weather['temperature']}°C")
            st.write(f"🌤️ **Condition:** {weather['weather']}")
        st.image(f"https://source.unsplash.com/800x400/?{city}", caption=city, use_column_width=True)
        st.write("---")

# Display Map
st.subheader("📍 Seven Sisters Map")
fig, ax = plt.subplots()
ax.scatter([lon for _, lon in cities.values()], [lat for lat, _ in cities.values()], c='red', label='Cities')
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Seven Sisters Location Map")
ax.legend()
buffer = BytesIO()
plt.savefig(buffer, format="png")
st.image(buffer, caption="Seven Sisters Map", use_column_width=True)
