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

def suggest_activities(weather, preferences):
    activities = []
    if "rain" in weather.lower():
        activities.extend(["Visit a local museum", "Explore a cultural center", "Try traditional cuisine at a restaurant"])
    else:
        activities.extend(["Go trekking in scenic trails", "Visit a famous temple or monastery", "Explore local markets"])
    
    if "relaxation" in preferences:
        activities.extend(["Enjoy a spa session", "Visit a scenic lake for peace and quiet", "Spend time in a wellness retreat"])
    if "food" in preferences:
        activities.extend(["Try street food specialties", "Dine at a traditional restaurant", "Join a local cooking class"])
    if "adventure" in preferences:
        activities.extend(["Go river rafting", "Try rock climbing", "Go camping in the hills"])
    
    return activities

def generate_itinerary(activities, num_days):
    itinerary = {}
    for day in range(1, num_days + 1):
        itinerary[f"Day {day}"] = activities[:3]  # Limit to 3 activities per day
    return itinerary

st.title("Seven Sisters Travel Itinerary Generator")

states = ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura"]
selected_state = st.selectbox("Select a state", states)
city = st.text_input("Enter a city")
arrival_date = st.date_input("Select your arrival date", datetime.date.today())
departure_date = st.date_input("Select your departure date", datetime.date.today())
arrival_time = st.time_input("Enter your arrival time")
departure_time = st.time_input("Enter your departure time")

preferences = st.multiselect("What kind of activities do you prefer?", ["relaxation", "food", "adventure", "culture", "nature"])

if arrival_date and departure_date:
    num_days = (departure_date - arrival_date).days + 1
else:
    num_days = 1

if st.button("Generate Itinerary"):
    if city:
        weather_data = get_weather(city)
        if weather_data:
            weather_desc = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            st.write(f"### Weather in {city} from {arrival_date} to {departure_date}:")
            st.write(f"Condition: {weather_desc.capitalize()}")
            st.write(f"Temperature: {temp}°C")
            
            activities = suggest_activities(weather_desc, preferences)
            itinerary = generate_itinerary(activities, num_days)
            st.write("### Your Travel Itinerary:")
            for day, act_list in itinerary.items():
                st.write(f"#### {day}")
                for activity in act_list:
                    st.write(f"- {activity}")
        else:
            st.error("Could not fetch weather data. Please check the city name.")
    else:
        st.warning("Please enter a city name.")
