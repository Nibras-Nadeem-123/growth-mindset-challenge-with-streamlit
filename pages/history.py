import streamlit as st
import json
import os

HISTORY_FILE = "data/challenge_history.json"

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

# Load history data
history = load_data(HISTORY_FILE)

st.title("📜 Challenge History")

name = st.text_input("Enter your name:")

if name:
    # ✅ Safe filtering to avoid KeyError
    user_history = [entry for entry in history if entry.get("user") == name]

    if user_history:
        st.subheader(f"Completed Challenges of {name}")
        for entry in user_history:
            challenge_text = entry.get("challenge", "Unknown Challenge")  # Handle missing 'challenge'
            date_text = entry.get("date", "Unknown Date")  # Handle missing 'date'
            st.write(f"✅ {challenge_text} (Completed on: {date_text})")
    else:
        st.info("No completed challenges yet.")
