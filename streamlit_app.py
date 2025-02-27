import streamlit as st
import json
import os
import random
from datetime import date, datetime, timedelta

PROGRESS_FILE = "progress.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_progress(filename, default_data=None):
    """Load progress data from a JSON file with default values."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):  # ✅ Ensure it's a dictionary
                    data.setdefault("streak_count", 0)
                    data.setdefault("best_streak", 0)
                    data.setdefault("last_completed_date", None)
                    data.setdefault("completed_challenges", [])
                    data.setdefault("custom_challenges", [])
                    return data
                else:
                    print(f"⚠ Warning: {filename} contains a list instead of a dictionary. Resetting...")
                    return default_data if default_data is not None else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return default_data if default_data is not None else {}
    return default_data if default_data is not None else {
        "streak_count": 0,
        "best_streak": 0,
        "last_completed_date": None,
        "completed_challenges": [],
        "custom_challenges": []
    }

def reset_streak(username, progress_data):
    progress_data["streak"] = 0
    save_progress(PROGRESS_FILE, progress_data)
    update_leaderboard(username, progress_data)
    if username in leaderboard:
        leaderboard[username]["streak"] = 0
        save_progress(LEADERBOARD_FILE, leaderboard)


# Default challenges
CHALLENGES = [
    "Read a motivational article.",
    "Write down three things you're grateful for.",
    "Learn a new skill for 15 minutes.",
    "Try a difficult task without fear of failure.",
    "Give someone a genuine compliment."
]

def get_daily_challenge():
    progress_data = load_progress(PROGRESS_FILE, {"last_date": "", "daily_challenge": ""})
    today = str(date.today())
    if progress_data.get("last_date") != today:
        progress_data["daily_challenge"] = random.choice(CHALLENGES)
        progress_data["last_date"] = today
        save_progress(PROGRESS_FILE, progress_data)
    return progress_data["daily_challenge"]

def update_leaderboard(username, progress_data):
    if not isinstance(progress_data, dict):  # ✅ Ensure it's a dictionary
        print(f"⚠ Warning: progress_data is {type(progress_data)} instead of dict. Resetting...")
        progress_data = {}

    leaderboard = {username: {"streak": data.get("streak", 0), "completed": data.get("completed", 0)}
    for username, data in progress_data.items() if isinstance(data, dict)}

    save_progress(LEADERBOARD_FILE, leaderboard)


def display_leaderboard():
    leaderboard = load_progress(LEADERBOARD_FILE, {})
    data = leaderboard_page()  # Call function to get data
    for item in data.items():  # Now data is a dictionary
        print(item)

    sorted_leaderboard = sorted(
    leaderboard_page.items(), 
    key=lambda x: (-int(x[1].get("streak", 0)), -int(x[1].get("completed", 0)))
)



    for rank, (user, stats) in enumerate(sorted_leaderboard, start=1):
        print(f"DEBUG: {user} -> {stats}")  # Print raw stats for debugging
    if not isinstance(stats, dict):
        st.write(f"{rank}. {user}: Invalid data format (not a dictionary)")
    elif "completed" not in stats or "streak" not in stats:
        st.write(f"{rank}. {user}: Missing keys in leaderboard data: {stats}")
    else:
        st.write(f"{rank}. {user}: {stats['completed']} completed, {stats['streak']} streak")

progress_data = load_progress(PROGRESS_FILE)

# Update streak logic
def update_streak(username):
    progress_data = load_progress(PROGRESS_FILE, {})
    user_data = progress_data.get(username , {"completed": 0, "streak": 0, "best_streak": 0, "last_completed": None})
    
    last_completed = user_data.get("last_completed")
    if last_completed:
        last_date = datetime.strptime(last_completed, "%Y-%m-%d").date()
        today = datetime.today().date()
        if today == last_date:
            st.warning("You've already completed today's challenge!")
            return user_data
        elif today - last_date == timedelta(days=1):
            user_data["streak"] += 1
        else:
            user_data["streak"] = 1  # Reset streak
    else:
        user_data["streak"] = 1  # First-time completion
    
    user_data["completed"] += 1
    user_data["last_completed"] = datetime.today().strftime("%Y-%m-%d")
    user_data["best_streak"] = max(user_data["streak"], user_data["best_streak"])
    
    progress_data[username] = user_data
    save_progress(PROGRESS_FILE, progress_data)
    return user_data



    # Ensure completed_challenges is a list
if not isinstance(progress_data.get("completed_challenges"), list):
        progress_data["completed_challenges"] = []


def save_progress(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f)
    
# Update leaderboard
def update_leaderboard(username, progress_data):
    progress_data = load_progress(PROGRESS_FILE, {})
    leaderboard = {username: {"streak": data.get("streak", 0), "completed": data.get("completed", 0)} for user, data in progress_data.items()}
    save_progress(LEADERBOARD_FILE, leaderboard)

    # if username not in leaderboard:
    #     leaderboard[username] = {"completed": 0, "streak": 0}

    # leaderboard[username]["streak"] = progress_data.get("streak_count", 0)
    # leaderboard[username]["completed"] = len(progress_data.get("completed_challenges", []))

    # save_progress(LEADERBOARD_FILE, leaderboard)

def leaderboard_page():
    st.subheader("🏆 Leaderboard - Top Performers")
    leaderboard = load_progress(LEADERBOARD_FILE, {})

    # ✅ Ensure sorted_leaderboard is always defined
    sorted_leaderboard = []

    if leaderboard:
        sorted_leaderboard = sorted(
            leaderboard.items(), key=lambda x: (-x[1]["streak"], -x[1]["completed"])
        )

    st.subheader("🏆 Leaderboard")

    if sorted_leaderboard:
        for idx, (user, data) in enumerate(sorted_leaderboard, start=1):
            st.write(f"{idx}. {user}: Streak - {data['streak']}, Completed - {data['completed']}")
    else:
        st.write("No leaderboard data available yet. Complete challenges to get on the leaderboard!")

    st.subheader("📌 Update Your Score")
    username = st.text_input("Enter your name to update leaderboard")

    if st.button("✅ Submit Progress"):
        if username:
            update_leaderboard(username)
            st.success(f"Leaderboard updated for {username}!")
        else:
            st.warning("Please enter a name before submitting.")

    return dict(sorted_leaderboard)  # ✅ Convert list of tuples back to dictionary

st.set_page_config(page_title="Growth Mindset Challenge", layout="wide", initial_sidebar_state="expanded")
st.title("🌱 Growth Mindset Challenge")
st.write("Welcome! Let's improve our skills through challenges and consistency.")

# Add Leaderboard Page
def leaderboard_page():
    st.subheader("🏆 Leaderboard - Top Performers")
    leaderboard = load_progress(LEADERBOARD_FILE, {})

    if leaderboard:
       sorted_leaderboard = sorted(
       [
        (user, stats) for user, stats in dict(sorted_leaderboard).items()
        if isinstance(stats, dict) and "streak" in stats and "completed" in stats
        ],
        key=lambda x: (-x[1]["streak"], -x[1]["completed"])
    )
    for rank, (user, streak) in enumerate(sorted_leaderboard, start=1):
        st.write(f"{rank}. {user}: {streak} days")

    else:
        st.write("No leaderboard data available yet. Complete challenges to get on the leaderboard!")

    st.subheader("📌 Update Your Score")
    username = st.text_input("Enter your name to update leaderboard")

    if st.button("✅ Submit Progress"):
        if username:
            update_leaderboard(username)
            st.success(f"Leaderboard updated for {username}!")
        else:
            st.warning("Please enter a name before submitting.")
    

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

def set_dark_mode():
    """Apply dark mode styles."""
    st.markdown(
        """
        <style>
            .main, .stApp, .block-container { background-color: #121212 !important; color: white !important; }
            div[data-testid="stSidebar"] { background-color: #1E1E1E !important; }
            button, select, input, textarea, selectbox { background-color: #2A2A2A !important; color: white !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

if dark_mode:
    set_dark_mode()

# Navigation
page = st.sidebar.selectbox("Select a Page", ["Daily Challenge", "Challenge History", "🎯 AI Recommendations", "🏆 Leaderboard"], key="secondary_page_selectbox")

if page == "Daily Challenge":
 # --- Load Progress --- #
    progress_data = load_progress(PROGRESS_FILE) 

    # --- List of challenges --- #
    challenges = [
    "Read 10 pages of a book",
    "Learn a new programming concept",
    "Solve one coding problem",
    "Write a daily journal entry",
    "Practice mindfulness for 10 minutes",
] + list(progress_data.get("custom_challenges", []))  # Add custom challenges


    st.subheader("➕ Add Your Own Challenge")
    new_challenge = st.text_input("Create a custom challenge:")
    if st.button("➕ Add Challenge") and new_challenge:
        progress_data["custom_challenges"].append(new_challenge)
        save_progress(PROGRESS_FILE, progress_data)
        st.success("Challenge added successfully!")
    else:
            st.warning("Please enter a challenge before adding.")


    # --- Daily Challenge System --- #
    today_date = datetime.now().strftime("%Y-%m-%d")
    if progress_data.get("last_date") != today_date:
        progress_data["daily_challenge"] = random.choice(challenges)
        progress_data["last_date"] = today_date
        save_progress(PROGRESS_FILE, progress_data)

    daily_challenge = random.choice(challenges)

    st.subheader("📅 Today's Challenge")
    st.write(f"👉 **{daily_challenge}**")

    if st.button("✅ Complete Daily Challenge"):
        # Ensure completed_challenges is a list, not a dict
        if not isinstance(progress_data.get("completed_challenges"), list):
            progress_data["completed_challenges"] = []

        # Now safely append the new challenge
        if daily_challenge not in progress_data["completed_challenges"]:
            progress_data["completed_challenges"].append(daily_challenge)

        update_streak()
        save_progress(PROGRESS_FILE, progress_data)
        st.success(f"Daily Challenge '{daily_challenge}' marked as completed!")

    # --- Select a challenge manually --- #
    selected_challenge = st.selectbox("Or choose a challenge manually", challenges)

    
    # --- Buttons to mark completion --- #
    
    if st.button("✅ Complete Selected Challenge"):
        if selected_challenge not in progress_data["completed_challenges"]:
            # Ensure completed_challenges is a list, not a dict
            if not isinstance(progress_data.get("completed_challenges"), list):
                progress_data["completed_challenges"] = []

    # Now safely append the new challenge
            if daily_challenge not in progress_data["completed_challenges"]:
                progress_data["completed_challenges"].append(daily_challenge)

            update_streak()
            save_progress(PROGRESS_FILE, progress_data)
            st.success(f"Selected Challenge '{selected_challenge}' marked as completed!")

    # --- Show Progress --- #
    st.subheader("📊 Your Progress")
    for challenge in progress_data["completed_challenges"]:
        st.write(f"- {challenge} ✅")

    st.write(f"🔥 **Current Streak:** {progress_data.get('streak_count', 0)} days")
    st.write(f"🏆 **Best Streak:** {progress_data.get('best_streak', 0)} days")

elif page == "Challenge History":
    st.subheader("📜 Challenge History")
    progress_data = load_progress(PROGRESS_FILE)
    completed_challenges = progress_data.get("completed_challenges", [])
    
    if completed_challenges:
        for challenge in completed_challenges:
            st.write(f"- {challenge} ✅")
    else:
        st.write("No challenges completed yet.")

elif page == "🎯 AI Recommendations":
    st.subheader("🎯 AI-Based Personalized Challenge Suggestions")
    progress_data = load_progress(PROGRESS_FILE)
    completed_challenges = set(progress_data.get("completed_challenges", []))

    # Suggest challenges based on completed ones
    challenge_pool = [
        "Read a research paper",
        "Build a small project with a new tech",
        "Write an article about a learning experience",
        "Practice meditation for 15 minutes",
        "Solve two coding problems",
    ]

    suggested_challenges = [ch for ch in challenge_pool if ch not in completed_challenges]
    if suggested_challenges:
        st.write("Based on your completed challenges, here are some recommendations:")
        for challenge in suggested_challenges:
            st.write(f"- {challenge}")
    else:
        st.write("You've completed all suggested challenges! Keep going!")

elif page == "🏆 Leaderboard":
    username = st.text_input("Enter your name:")
    if username and username.isalnum():
        st.write(f"👋 Welcome, {username}!")
        st.write(f"📌 Today's Challenge: {get_daily_challenge()}")
    
    if st.button("✔ Mark as Completed"):
        update_leaderboard(username, progress_data)
        st.success("Challenge Completed! Keep going! 🔥")
    
    if st.button("❌ Reset Streak"):
        reset_streak(username)
        st.warning("Your streak has been reset.")
    quotes = [
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
        "Your time is limited, so don’t waste it living someone else’s life."
    ]

    tips = [
        "Set clear goals and work towards them daily.",
        "Practice gratitude every morning to start your day positively.",
        "Take breaks and practice mindfulness to stay focused."
    ]

    # Select random daily quote and tip
    random.seed(date.today().toordinal())
    daily_quote = random.choice(quotes)
    daily_tip = random.choice(tips)
    def load_leaderboard():
        try:
             with open("leaderboard.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
             return {}
 
 
    # Motivational Quotes & Tips Section
    st.header("🌟 Daily Motivation")
    st.write(f"**Quote of the Day:** {daily_quote}")
    st.write(f"**Tip:** {daily_tip}")

    # Main challenge section
    st.header("🚀 Today's Challenge")
    st.write("Complete your challenge to increase your progress!")
    leaderboard = load_leaderboard()
    progress = load_progress(PROGRESS_FILE)
 
    # Save leaderboard
    def save_leaderboard(leaderboard):
        with open("leaderboard.json", "w") as f:
            json.dump(leaderboard, f)
 
    if username:
        if st.button("Mark Challenge as Completed"):
            if username not in progress:
                progress[username] = {"streak": 0, "completed": 0}

            progress[username]["streak"] += 10
            leaderboard[username] = progress[username]
            save_progress(PROGRESS_FILE, progress_data)
            save_leaderboard(leaderboard)
            st.success("Challenge marked as completed! Your progress has been updated.")



        st.subheader("🏆 Leaderboard")
    display_leaderboard()
else:
    st.warning("Please enter a valid name (letters & numbers only).")



 



 

