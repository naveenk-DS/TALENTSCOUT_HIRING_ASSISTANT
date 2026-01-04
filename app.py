import streamlit as st
import requests
import os
import re
import time
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
# # OPENAI CONFIG
# # =============================
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# =============================
# SESSION STATE
# =============================
# if "step" not in st.session_state:
#     st.session_state.step = 0
#     st.session_state.data = {}
#     st.session_state.messages = []


if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

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

fields = [
    "name",
    "email",
    "phone",
    "experience",
    "position",
    "location",
    "tech_stack"
]



exit_words = ["exit", "quit", "bye", "goodbye"]

# =============================
# FUNCTIONS
# =============================
def is_exit(text):
    return text.lower().strip() in exit_words

def generate_technical_questions(tech_stack):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
    }

    prompt = (
        "You are a technical interviewer.\n\n"
        f"Candidate tech stack:\n{tech_stack}\n\n"
        "Generate 3–5 technical interview questions for EACH technology.\n"
        "Questions should test practical, real-world knowledge.\n"
        "Group questions by technology."
    )

    payload = {"inputs": prompt}

    # Retry mechanism (important for Hugging Face free tier)
    for _ in range(3):
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        # ✅ Successful response
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        # 🔄 Model loading → wait and retry
        if isinstance(result, dict) and "error" in result:
            time.sleep(2)
            continue

    return "Technical questions could not be generated right now. Please try again."



# use only primary 


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and 10 <= len(phone) <= 13


def bot_reply(user_input):
    step = st.session_state.step
    user_data = st.session_state.user_data

    # EMAIL (PRIMARY)
    if step == 1:
        if not is_valid_email(user_input):
            return "❌ Please enter a valid email address."
        user_data["email"] = user_input
        st.session_state.step += 1
        return questions[st.session_state.step]

    # PHONE (PRIMARY)
    if step == 2:
        if not is_valid_phone(user_input):
            return "❌ Please enter a valid phone number (digits only)."
        user_data["phone"] = user_input
        st.session_state.step += 1
        return questions[st.session_state.step]

    # NORMAL FLOW
    user_data[fields[step]] = user_input
    st.session_state.step += 1

    if st.session_state.step < len(questions):
        return questions[st.session_state.step]

    # TECH STACK → GENERATE QUESTIONS
    tech_stack = user_data["tech_stack"]
    technical_questions = generate_technical_questions(tech_stack)
    return f"Here are your technical interview questions:\n\n{technical_questions}"

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
