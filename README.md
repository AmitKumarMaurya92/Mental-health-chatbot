# AI Voice-Based Mental Health Companion

An AI-powered mental health chatbot built with Python, FastAPI, and OpenAI. It aims to provide a gentle, supportive, and safe conversational experience with emotion-sensitive responses and built-in safety checks.

## Current Progress

- [x] **Step 1:** Text chatbot (AI API working)
- [x] **Step 2:** Add sentiment analysis
- [x] **Step 3:** Add safety checks
- [x] **Step 4:** Add suggestions
- [x] **Step 5:** Add voice input/output
- [ ] **Step 6:** Add memory (context)
- [ ] **Step 7:** Optional UI

## Features
- **Human-like Conversation**: Uses OpenAI API for intelligence.
- **Emotion-Sensitive**: Upcoming feature to detect mood and adapt tone.
- **Voice Capabilities**: Upcoming feature for hands-free speech input/output.
- **Safety**: Built-in rules to detect crisis situations.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key in a `.env` file:
   ```env
   OPENAI_API_KEY=your_key_here
   ```
3. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

*(Note: This README will be updated continuously as new features are added)*
