import json

# Load progress
def load_progress(user):
    try:
        with open("progress.json", "r") as file:
            data = json.load(file)
        return data.get(user, {"streak": 0, "completed_challenges": 0, "last_completed": ""})
    except FileNotFoundError:
        return {"streak": 0, "completed_challenges": 0, "last_completed": ""}

# Save progress
def save_progress(user, progress):
    try:
        with open("progress.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[user] = progress
    with open("progress.json", "w") as file:
        json.dump(data, file)

# Update Leaderboard
def update_leaderboard(user, challenges_completed):
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = {}

    leaderboard[user] = challenges_completed
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)

# Get Leaderboard Data
def get_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
