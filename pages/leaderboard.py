import os
import streamlit as st
import json
import random

LEADERBOARD_FILE = "data/leaderboard.json"
USER_DATA_FILE = "data/users.json"

# Load user data
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

users = load_users()

# Load leaderboard data
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

leaderboard = load_leaderboard()

st.title("🏆 Leaderboard")

# Sort users by completed challenges
sorted_users = sorted(users.items(), key=lambda x: x[1]['completed_challenges'], reverse=True)

# Random Motivational Quotes
QUOTES = [
    "Believe in yourself and all that you are! 🌟",
    "Your only limit is your mind. 💡",
    "Success is the sum of small efforts, repeated daily. 🔥",
    "Dream big and dare to fail! 🚀",
    "Keep pushing forward! You're stronger than you think! 💪",
]

if not leaderboard:
    st.warning("No completed challenges yet.")
else:
    for idx, (user, data) in enumerate(sorted_users, start=1):
        st.subheader(f"🥇 {idx}. {user} (Completed Challenges: {data['completed_challenges']})")
        
        user_challenges = [entry for entry in leaderboard if entry["user"] == user]
        
        if user_challenges:
            for entry in user_challenges:
                st.write(f"✅ **{entry['challenge']}** - Completed on {entry['date']}")
            
            # 🎯 Show a motivational quote after listing the user's challenges
            st.info(random.choice(QUOTES))
        else:
            st.write("No challenges completed yet.")
