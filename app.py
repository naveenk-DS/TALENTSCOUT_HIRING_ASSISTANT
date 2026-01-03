import streamlit as st
import openai
import os

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 TalentScout Hiring Assistant")
st.caption("AI-powered initial screening chatbot")

# =============================
# OPENAI CONFIG
# =============================
openai.api_key = os.getenv("OPENAI_API_KEY")

# =============================
# SESSION STATE
# =============================
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.messages = []

# =============================
# QUESTIONS FLOW
# =============================
questions = [
    "What is your full name?",
    "What is your email address?",
    "What is your phone number?",
    "How many years of professional experience do you have?",
    "Which position(s) are you applying for?",
    "What is your current location?",
    "Please list your tech stack (languages, frameworks, databases, tools)."
]

exit_words = ["exit", "quit", "bye", "goodbye"]

# =============================
# FUNCTIONS
# =============================
def is_exit(text):
    return text.lower().strip() in exit_words

def generate_technical_questions(tech_stack):
    prompt = f"""
You are a technical interviewer.

Candidate tech stack:
{tech_stack}

Generate 3–5 interview questions per technology.
Questions should assess practical and real-world knowledge.
Group questions clearly by technology.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",   # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    return response.choices[0].message.content

def bot_reply(user_input):
    if is_exit(user_input):
        return "Thank you for your time! 👋 Our recruitment team will contact you soon."

    step = st.session_state.step

    if step < len(questions):
        st.session_state.data[questions[step]] = user_input
        st.session_state.step += 1

        if st.session_state.step < len(questions):
            return questions[st.session_state.step]
        else:
            tech_stack = st.session_state.data[questions[-1]]
            tech_questions = generate_technical_questions(tech_stack)
            st.session_state.step += 1
            return (
                "✅ Thank you for providing your details.\n\n"
                "Here are your technical interview questions:\n\n"
                f"{tech_questions}"
            )

    return "Thank you! We will review your profile and get back to you."

# =============================
# INITIAL MESSAGE
# =============================
if not st.session_state.messages:
    welcome = (
        "Hello! 👋 I’m the **TalentScout Hiring Assistant**.\n\n"
        "I’ll collect your basic details and then ask technical questions "
        "based on your tech stack.\n\n"
        "Type **exit** anytime to end the conversation.\n\n"
        f"{questions[0]}"
    )
    st.session_state.messages.append(("bot", welcome))

# =============================
# CHAT UI
# =============================
for role, message in st.session_state.messages:
    st.chat_message(role).write(message)

user_input = st.chat_input("Type your response here...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    response = bot_reply(user_input)
    st.session_state.messages.append(("bot", response))
    st.rerun()
