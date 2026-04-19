# AI Voice-Based Mental Health Companion

An AI-powered mental health chatbot built with Python, FastAPI, and Google Gemini. It aims to provide a gentle, supportive, and safe conversational experience with emotion-sensitive responses and built-in safety checks.

## Current Progress

- [x] **Step 1:** Text chatbot (AI API working)
- [x] **Step 2:** Add sentiment analysis
- [x] **Step 3:** Add safety checks
- [x] **Step 4:** Add suggestions
- [x] **Step 5:** Add voice input/output
- [x] **Step 6:** Add memory (context)
- [x] **Step 7:** Optional UI

## Features
- **Human-like Conversation**: Uses Google Gemini API for intelligence.
- **Emotion-Sensitive**: Upcoming feature to detect mood and adapt tone.
- **Voice Capabilities**: Upcoming feature for hands-free speech input/output.
- **Safety**: Built-in rules to detect crisis situations.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Gemini API keys in a `.env` file:
   ```env
   GEMINI_API_KEY_1=your_key_1
   GEMINI_API_KEY_2=your_key_2
   GEMINI_API_KEY_3=your_key_3
   ```
3. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

*(Note: This README will be updated continuously as new features are added)*
