import streamlit as st
import openai # type: ignore
import random

# OpenAI API Key
openai.api_key = "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"  # Apni API key yahan paste karein

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

def chat_with_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ya jo bhi latest model ho
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

if st.button("Ask AI"):
    if user_input:
        ai_response = chat_with_ai(user_input)
        st.write(f"🤖 AI: {ai_response}")
    else:
        st.warning("Please enter a question!")

