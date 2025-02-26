import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# OpenWeatherMap API Key (Replace with your actual key)
API_KEY = "YOUR_API_KEY"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Sample activity database
activities = {
    "Sightseeing": {
        "good": ["Visit historical sites", "Explore local markets", "Visit museums"],
        "bad": ["Visit an art gallery", "Indoor cultural performance", "Attend a local workshop"]
    },
    "Adventure": {
        "good": ["Hiking", "Water sports", "Skydiving"],
        "bad": ["Indoor rock climbing", "Virtual reality gaming", "Escape room challenge"]
    },
    "Food & Culture": {
        "good": ["Try local cuisine", "Visit food markets", "Attend cultural shows"],
        "bad": ["Cooking class", "Wine tasting", "Museum tour"]
    },
    "Relaxation": {
        "good": ["Spa day", "Beach relaxation", "Yoga retreat"],
        "bad": ["Hotel spa & wellness", "Book reading in a cozy café", "Movie night"]
    },
}

# Function to fetch real-time weather
def get_weather(destination):
    params = {"q": destination, "appid": API_KEY, "units": "metric"}
    response = requests.get(WEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        condition = data['weather'][0]['main'].lower()

        # Determine if weather is bad
        bad_weather_conditions = ["rain", "storm", "snow", "extreme", "thunderstorm"]
        weather_status = "bad" if any(cond in condition for cond in bad_weather_conditions) else "good"

        weather = {
            "Temperature": f"{data['main']['temp']}°C",
            "Condition": data['weather'][0]['description'].title(),
            "Humidity": f"{data['main']['humidity']}%",
            "Wind Speed": f"{data['wind']['speed']} m/s",
            "Status": weather_status
        }
        return weather
    else:
        return None

# Function to generate an itinerary based on weather
def generate_itinerary(destination, start_date, end_date, interests, weather_status):
    days = (end_date - start_date).days + 1
    itinerary = []
    
    for i in range(days):
        day = start_date + timedelta(days=i)
        day_plan = {"Day": f"Day {i+1} ({day.strftime('%A')})", "Activities": []}
        
        for interest in interests:
            if interest in activities:
                # Adjust activities based on weather
                day_plan["Activities"].append(activities[interest][weather_status][i % len(activities[interest][weather_status])])
        
        itinerary.append(day_plan)
    
    return itinerary

# Function to save itinerary as PDF
def save_itinerary_pdf(destination, itinerary, weather):
    pdf_filename = f"{destination}_itinerary.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Travel Itinerary for {destination}")

    y_position = 730
    c.drawString(100, y_position, f"Weather: {weather['Temperature']}, {weather['Condition']}")

    y_position -= 30
    for day in itinerary:
        y_position -= 30
        c.drawString(100, y_position, day["Day"])
        y_position -= 20
        for activity in day["Activities"]:
            c.drawString(120, y_position, f"- {activity}")
            y_position -= 20

    c.save()
    return pdf_filename

# Streamlit App
st.set_page_config(page_title="🗺️ Smart Itinerary Planner", layout="wide")

st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🗺️ Smart Itinerary Planner</h1>", unsafe_allow_html=True)

# User Inputs
destination = st.text_input("Enter your destination:", "Goa")
start_date = st.date_input("Start Date", datetime.today())
end_date = st.date_input("End Date", datetime.today() + timedelta(days=3))
budget = st.slider("Budget (INR)", 5000, 50000, 15000, step=5000)
interests = st.multiselect("Select your interests:", list(activities.keys()), default=["Sightseeing"])

if st.button("Generate Itinerary"):
    if start_date > end_date:
        st.error("End Date should be after Start Date!")
    else:
        weather = get_weather(destination)

        if not weather:
            st.warning("⚠️ Could not fetch weather data. Please check the city name.")
            weather_status = "good"
        else:
            weather_status = weather["Status"]

        itinerary = generate_itinerary(destination, start_date, end_date, interests, weather_status)

        # Display Weather
        st.subheader(f"🌤️ Weather in {destination}")
        st.write(f"**Temperature:** {weather['Temperature']}")
        st.write(f"**Condition:** {weather['Condition']}")
        st.write(f"**Humidity:** {weather['Humidity']}")
        st.write(f"**Wind Speed:** {weather['Wind Speed']}")
        st.write(f"**Weather Status:** {'🌧️ Bad Weather - Adjusted Plan' if weather_status == 'bad' else '☀️ Good Weather'}")

        # Display Itinerary
        st.subheader(f"📍 Itinerary for {destination}")
        for day in itinerary:
            st.markdown(f"### {day['Day']}")
            for activity in day["Activities"]:
                st.markdown(f"- {activity}")

        # Download Option
        pdf_file = save_itinerary_pdf(destination, itinerary, weather)
        with open(pdf_file, "rb") as file:
            st.download_button(label="📥 Download Itinerary", data=file, file_name=pdf_file, mime="application/pdf")
