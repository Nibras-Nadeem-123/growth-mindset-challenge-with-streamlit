import streamlit as st
import json
import os
import pandas as pd
import altair as alt
import random

# File Paths
USER_DATA_FILE = "data/users.json"
HISTORY_FILE = "data/challenge_history.json"

# Motivational Quotes
QUOTES = [
    "Believe in yourself and all that you are! 🌟",
    "Your only limit is your mind. 💡",
    "Success is the sum of small efforts, repeated daily. 🔥",
    "Every challenge you complete brings you closer to success. 🚀",
    "Keep pushing forward, greatness takes time! 💪"
]

# Function to load user data
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to load challenge history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Load data
users = load_users()
history = load_history()

st.title("📊 Your Daily Progress Chart")

name = st.text_input("Enter your name:")
if name:
    if name not in users:
        st.warning("No data found for this user.")
    else:
        st.subheader(f"Welcome, {name}! Keep up the great work! 🎯")
        
        # Filter user-specific challenge history
        user_history = [entry for entry in history if entry.get("user") == name]
        
        if user_history:
            # Convert data to DataFrame
            df = pd.DataFrame(user_history)
            df["date"] = pd.to_datetime(df["date"])  # Ensure date is in datetime format
            
            # Group data to count challenges per day
            daily_counts = df.groupby(["date", "challenge"]).size().reset_index(name="Completed Challenges")
            
            # Create a multi-line chart
            chart = alt.Chart(daily_counts).mark_line(point=True).encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("Completed Challenges:Q", title="Number of Challenges"),
                color=alt.Color("challenge:N", title="Challenge Type"),  # Different colors for each challenge
                tooltip=["date:T", "challenge:N", "Completed Challenges"]
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            
            # Display motivational quote
            st.info(random.choice(QUOTES))
        else:
            st.info("No completed challenges yet.")
            st.info(random.choice(QUOTES))
