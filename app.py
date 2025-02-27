import streamlit as st
import json
import os
import datetime
import random

# File Paths
CHALLENGE_FILE = "data/user_challenges.json"
DAILY_FILE = "data/daily_challenges.json"
HISTORY_FILE = "data/challenge_history.json"
LEADERBOARD_FILE = "data/leaderboard.json"
USER_DATA_FILE = "data/users.json"

# Function to load user data
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save user data
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Load users
users = load_users()
# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Initialize Files
for file in [CHALLENGE_FILE, DAILY_FILE, HISTORY_FILE, LEADERBOARD_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

# Load Data
def load_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

# Save Data
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Load Existing Challenges
challenges = load_data(CHALLENGE_FILE)
history = load_data(HISTORY_FILE)
leaderboard = load_data(LEADERBOARD_FILE)

# --- 🎯 DAILY CHALLENGE LOGIC ---
DAILY_CHALLENGES = [
    "Write down 3 things you're grateful for 🙏",
    "Exercise for 15 minutes today 🏋️",
    "Read 10 pages of a book 📖",
    "Avoid social media for 1 hour 📵",
    "Drink 8 glasses of water today 💧",
]

today_date = str(datetime.date.today())
daily_data = load_data(DAILY_FILE)

# If there's no challenge for today, pick a new one
if not daily_data or daily_data.get("date") != today_date:
    new_daily = random.choice(DAILY_CHALLENGES)
    daily_data = {"date": today_date, "challenge": new_daily, "completed": False}
    save_data(DAILY_FILE, daily_data)
else:
    new_daily = daily_data["challenge"]

# --- 🔥 MOTIVATIONAL QUOTES ---
QUOTES = [
    "Believe in yourself and all that you are! 🌟",
    "Your only limit is your mind. 💡",
    "Success is the sum of small efforts, repeated daily. 🔥",
    "Dream big and dare to fail! 🚀",
    "Keep pushing forward! You're stronger than you think! 💪",
    "The future depends on what you do today. 🌎",
    "Mistakes are proof that you are trying. 💯",
    "Push yourself because no one else is going to do it for you! 🏆",
]

# --- 🏡 MAIN APP INTERFACE ---
st.title("💡 Growth Mindset Challenge")

name = st.text_input("Enter your name:")
if name:
    if name not in users:
        users[name] = {"completed_challenges": 0, "challenges": []}
        save_users(users)
    st.success(f"Welcome, {name}!")

st.info(random.choice(QUOTES))  # 🎯 Show a motivational quote

# --- 🎯 DAILY CHALLENGE SECTION ---
st.subheader("🌟 Today's Challenge")
st.write(f"🗓 **{today_date}**")
st.info(f"📌 **Challenge:** {new_daily}")

if not daily_data["completed"]:
    if st.button("✅ Mark Daily Challenge as Completed"):
        daily_data["completed"] = True
        leaderboard.append({"challenge": new_daily, "user": name, "date": today_date})
        save_data(DAILY_FILE, daily_data)
        save_data(LEADERBOARD_FILE, leaderboard)
        st.success("Daily Challenge Completed! 🎉")

st.info(random.choice(QUOTES))  # 🎯 Show a motivational quote

# --- ✅ CUSTOM CHALLENGES ---
st.subheader("Create Your Own Challenge")
new_challenge = st.text_input("Enter a new challenge:")

if st.button("Add Challenge"):
    if new_challenge.strip():
        challenges.append(new_challenge)
        history.append({"challenge": new_challenge, "date": today_date})
        save_data(CHALLENGE_FILE, challenges)
        save_data(HISTORY_FILE, history)
        st.success("Challenge added successfully!")

st.info(random.choice(QUOTES))  # 🎯 Show a motivational quote

# --- 🔥 SELECT & COMPLETE A CHALLENGE ---
st.subheader("Your Challenges")
if challenges:
    selected_challenge = st.selectbox("Choose a challenge:", challenges)

    if st.button("Complete Challenge"):
        # ✅ Challenge ko leaderboard aur history dono mein add karein
        leaderboard.append({"challenge": selected_challenge, "user": name, "date": today_date})
        history.append({"user": name, "challenge": selected_challenge, "date": today_date})

        # ✅ User data update karein (profile ke liye)
        users[name]["completed_challenges"] += 1
        users[name]["challenges"].append(selected_challenge)  # Store completed challenges

        # ✅ Save updates
        challenges.remove(selected_challenge)
        save_data(CHALLENGE_FILE, challenges)
        save_data(LEADERBOARD_FILE, leaderboard)
        save_data(HISTORY_FILE, history)
        save_users(users)

        st.success("Challenge marked as completed! 🎉")

st.info(random.choice(QUOTES))  # 🎯 Show a motivational quote

# --- 📌 SIDEBAR NAVIGATION ---
st.sidebar.page_link("pages/profile.py", label="My Profile")
st.sidebar.page_link("pages/leaderboard.py", label="🏆 View Leaderboard")
st.sidebar.page_link("pages/history.py", label="📜 View Challenge History")
st.sidebar.page_link("pages/ai_recommendations.py", label="🤖 AI Recommendations")
