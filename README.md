# TalentScout – Intelligent Hiring Assistant Chatbot

## Project Overview

TalentScout Hiring Assistant is an intelligent, conversational chatbot designed to assist recruiters during the **initial screening phase** of technical hiring.  
The chatbot collects essential candidate information and dynamically generates **technology-specific interview questions** based on the candidate’s declared tech stack.

This project demonstrates:
- Prompt engineering with Large Language Models (LLMs)
- Context-aware conversational flow
- Secure handling of sensitive information
- Deployment of an AI-powered application

---

## Key Features

### Candidate Information Collection
The chatbot collects the following candidate details:
- Full Name  
- Email Address (**mandatory & validated**)  
- Phone Number (**mandatory & validated**)  
- Years of Professional Experience  
- Desired Position(s)  
- Current Location  
- Tech Stack (languages, frameworks, databases, tools)

### Tech Stack–Aware Question Generation
- Generates **3–5 technical interview questions per technology**
- Questions focus on **practical, real-world knowledge**
- Questions are grouped clearly by technology

### Conversational Intelligence
- Maintains conversation context
- Handles unexpected inputs gracefully
- Supports exit keywords (`exit`, `quit`, `bye`)
- Provides meaningful fallback responses

### Security & Privacy
- No API keys or sensitive data are hardcoded
- API keys are managed using **environment variables**
- Candidate data is handled in-memory (simulated storage)
- Designed with data privacy best practices in mind

---

## Technology Stack

| Component | Technology |
|--------|-----------|
| Programming Language | Python |
| Frontend Framework | Streamlit |
| LLM Provider | Hugging Face Inference API |
| Model Used | google/flan-t5-large |
| Deployment Platform | Render |
| Version Control | Git & GitHub |

---

## Application Architecture

-User
   ↓
-Streamlit UI
   ↓
-Conversation & Validation Logic
    ↓
-Prompt Engineering Layer
    ↓
-Hugging Face Inference API
    ↓
-Generated Technical Questions


---

## Prompt Design

The LLM is guided using structured prompts that:
- Define the role of the model as a *technical interviewer*
- Include the candidate’s declared tech stack
- Explicitly request **3–5 questions per technology**
- Emphasize practical, real-world assessment

Example prompt:
-  Generate 3–5 technical interview questions for each technology.
Group questions clearly by technology.
Focus on practical, real-world knowledge.


---

## Validation Rules

| Field | Rule |
|----|----|
| Email | Valid email format required |
| Phone | Digits only (10–13 characters) |
| Tech Stack | Mandatory input |

The chatbot does not proceed unless mandatory fields are valid.

---

## Installation (Local Setup)

```bash
git clone https://github.com/<your-username>/TALENTSCOUT_HIRING_ASSISTANT.git
cd TALENTSCOUT_HIRING_ASSISTANT
pip install -r requirements.txt
streamlit run app.py

