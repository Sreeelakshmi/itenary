import streamlit as st
import requests
import datetime

def get_weather(city):
    API_KEY = "f8cb952227a9226d7088520604acec5a"  # Replace with your OpenWeather API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def suggest_activities(weather):
    if "rain" in weather.lower():
        return ["Visit a local museum", "Explore a cultural center", "Try traditional cuisine at a restaurant"]
    else:
        return ["Go trekking in scenic trails", "Visit a famous temple or monastery", "Explore local markets"]

st.title("Seven Sisters Travel Itinerary Generator")

states = ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura"]
selected_state = st.selectbox("Select a state", states)
city = st.text_input("Enter a city")
date = st.date_input("Select your travel date", datetime.date.today())

if st.button("Generate Itinerary"):
    if city:
        weather_data = get_weather(city)
        if weather_data:
            weather_desc = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            st.write(f"### Weather in {city} on {date}:")
            st.write(f"Condition: {weather_desc.capitalize()}")
            st.write(f"Temperature: {temp}°C")
            
            activities = suggest_activities(weather_desc)
            st.write("### Recommended Activities:")
            for activity in activities:
                st.write(f"- {activity}")
        else:
            st.error("Could not fetch weather data. Please check the city name.")
    else:
        st.warning("Please enter a city name.")
