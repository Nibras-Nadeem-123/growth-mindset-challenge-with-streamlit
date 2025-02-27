import streamlit as st
import random

st.title("🤖 AI Recommended Challenges")

AI_CHALLENGES = [
    "Read a new book this week 📖",
    "Practice gratitude daily 🙏",
    "Learn a new skill online 🎓",
    "Meditate for 10 minutes daily 🧘‍♂️"
]

random_challenge = random.choice(AI_CHALLENGES)
st.write(f"🔮 **Recommended Challenge:** {random_challenge}")

st.subheader("Chat with AI Bot")
user_input = st.text_input("Ask anything related to personal growth:")

if st.button("Ask AI"):
    st.write(f"🤖 AI: {random.choice(['Stay consistent!', 'Growth takes time, keep going!', 'Challenges make you stronger!'])}")
