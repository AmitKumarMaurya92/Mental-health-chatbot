# AI Voice-Based Mental Health Companion ✨

An empathetic, AI-powered mental health companion built with **Python**, **FastAPI**, and **Google Gemini 1.5 Flash**. This companion provides a gentle, supportive space with emotion-sensitive responses, real-time safety checks, seamless voice interaction, and persistent mood tracking.

![UI Screenshot](https://raw.githubusercontent.com/AmitKumarMaurya92/Mental-health-chatbot/main/ui/static/screenshot_mockup.png)

## 🌟 Key Features

- **🔐 Secure Authentication**: Multi-user support with encrypted password hashing (BCrypt) and secure session-based isolation.
- **🧠 Empathetic AI**: Powered by Google Gemini 1.5 Flash for nuanced, supportive dialogue tailored to your emotional needs.
- **🎭 Emotion-Driven UI**: Real-time sentiment analysis that dynamically shifts the glassmorphic UI theme to match your mood (Happy, Sad, Neutral).
- **📊 Mood Analytics**: Interactive dashboard with Chart.js to track emotional trends and mood scores over a 7-day period.
- **🎙️ Seamless Voice**: Integrated Web Speech API for natural voice-to-text input and text-to-voice responses.
- **📝 Weekly Summaries**: AI-generated reports that summarize your emotional journey and provide personalized progress insights.
- **🛡️ Secure Data Isolation**: Strict per-user data scoping ensures your chat history and mood logs are strictly private.
- **🗑️ Account Management**: Take full control of your privacy with the ability to permanently delete your account and all associated data.
- **📱 Responsive Design**: Fully refactored UI for a stable and aesthetically pleasing experience on both desktop and mobile devices.
- **💡 Coping Strategies**: Integrated suggestion service providing breathing exercises and grounding techniques when needed.
- **📔 AI Journaling**: Dedicated space for personal reflections with empathetic AI feedback on every entry.

## ⚙️ How It Works

1.  **Input**: Users interact via text or voice (Web Speech API).
2.  **Emotion Processing**: Every message is analyzed using `vaderSentiment` and custom heuristics to detect emotional nuances.
3.  **AI Orchestration**: Context-aware prompts are sent to Gemini to generate supportive, therapeutic-style responses.
4.  **Reactive UI**: The interface updates dynamically, changing colors and animations based on detected emotions to create an immersive experience.
5.  **Persistence & Privacy**: All interactions and mood scores are securely stored in a local SQLite database with strict session-based access control.

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, Starlette (Sessions), Pydantic |
| **AI/ML** | Google Gemini 1.5 Flash, VADER Sentiment |
| **Database** | SQLite, SQLAlchemy |
| **Security** | BCrypt, Passlib, ItsDangerous |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JS, Jinja2 |
| **Visualization** | Chart.js |

## 🚀 Setup & Installation

### **1. Prerequisites**
- Python 3.10+
- Google AI Studio API Key ([Get it here](https://aistudio.google.com/))

### **2. Local Installation**
```bash
git clone https://github.com/AmitKumarMaurya92/Mental-health-chatbot.git
cd mental-health-chatbot
python -m venv .venv
# Activate venv (Windows: .venv\Scripts\activate | Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

### **3. Configuration**
Create a `.env` file in the root:
```env
GEMINI_API_KEY_1=your_api_key_here
```

### **4. Run**
```bash
python app.py
```
Visit `http://localhost:8000`.

## ☁️ Deployment (Render)

This app is optimized for deployment on [Render](https://render.com).

1.  **Environment Variables**: Add `GEMINI_API_KEY_1` in the Render dashboard.
2.  **Build Command**: `pip install -r requirements.txt`
3.  **Start Command**: `gunicorn -w 1 -k uvicorn.workers.UvicornWorker --timeout 120 app:app`

## 📁 Project Structure
```text
├── app.py                     # Main FastAPI entry point & Routing
├── services/                  # Business logic (AI, Sentiment, DB, Suggestions)
├── dashboard/                 # Analytics & Mood summary generation
├── ui/                        # Templates (Jinja2) and Static assets (CSS, JS)
├── data/                      # SQLite database storage
├── voice/                     # Voice input (STT) and output (TTS) handlers
├── utils/                     # Security helpers (BCrypt) and Utility scripts
├── prompts/                   # Context-aware AI instruction templates
├── tests/                     # Unit and integration tests
└── scratch/                   # Development scripts and DB management tools
```

---
***Disclaimer**: This AI is for companionship and emotional support only. It is NOT a replacement for professional medical advice, diagnosis, or treatment. If you are in a crisis, please contact local emergency services immediately.*


