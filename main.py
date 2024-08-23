import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew
from textwrap import dedent
from agents import TravelAgents
from tasks import TravelTasks

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Import DuckDuckGoSearchRun from langchain-community
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize search tool
search_tool = DuckDuckGoSearchRun()

# Set environment variables from .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        agents = TravelAgents()
        tasks = TravelTasks()

        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent,
            self.cities,
            self.date_range,
            self.interests
        )

        gather_city_info = tasks.gather_city_info(
            local_tour_guide,
            self.cities,
            self.date_range,
            self.interests
        )

        identify_city = tasks.identify_city(
            city_selection_expert,
            self.origin,
            self.cities,
            self.date_range,
            self.interests
        )

        crew = Crew(
            agents=[expert_travel_agent, city_selection_expert, local_tour_guide],
            tasks=[plan_itinerary, gather_city_info, identify_city],
            verbose=True,
        )

        result = crew.kickoff()
        return result

def main():
    # Set page configuration
    st.set_page_config(page_title="Trip Planner", page_icon="🌍", layout="wide")

    # Apply custom CSS
    st.markdown("""
        <style>
        .reportview-container {
            background: #f0f8ff;
        }
        .sidebar .sidebar-content {
            background: #e0f7fa;
        }
        .css-18e3th9 {
            background: #00796b;
            color: white;
        }
        .css-1f6h6k5 {
            background: #004d40;
            color: white;
        }
        .css-1ki2jl0 {
            color: #004d40;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("Trip Planner")
    st.sidebar.image("https://images.unsplash.com/photo-1506748686214e9df14a2e4d7f15d0a80e9b1c35b7e7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fHRyYXZlbHxlbnwwfHx8fDE2NjUyMzk4MTg&ixlib=rb-1.2.1&q=80&w=400", use_column_width=True)
    st.sidebar.write("## Plan Your Perfect Trip")

    # Main content
    st.title("Welcome to Your Personalized Trip Planner")
    st.write("### Create Your Ultimate Travel Itinerary")

    # Input fields for travel details
    st.subheader("Travel Details")
    origin = st.text_input("Starting Location", "e.g., Paris, France")
    cities = st.text_input("Cities to Visit", "e.g., Rome, Barcelona, Athens")
    date_range = st.text_input("Date Range", "e.g., July 1, 2024 - July 15, 2024")
    interests = st.text_input("Your Interests", "e.g., historical sites, beaches, gourmet dining")

    if st.button("Generate Itinerary"):
        if origin and cities and date_range and interests:
            cities_list = [city.strip() for city in cities.split(',')]
            interests_list = [interest.strip() for interest in interests.split(',')]
            
            custom_crew = TripCrew(origin, cities_list, date_range, interests_list)
            result = custom_crew.run()
            
            st.write("## Here is Your Custom Travel Itinerary:")
            st.write(result)
        else:
            st.error("Please fill in all the fields.")

if __name__ == "__main__":
    main()
