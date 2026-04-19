# AI Voice-Based Mental Health Companion ✨

An empathetic, AI-powered mental health companion built with **Python**, **FastAPI**, and **Google Gemini 1.5 Flash**. This companion provides a gentle, supportive space with emotion-sensitive responses, real-time safety checks, seamless voice interaction, and persistent mood tracking.

![UI Screenshot](https://raw.githubusercontent.com/AmitKumarMaurya92/Mental-health-chatbot/main/ui/static/screenshot_mockup.png)

## 🌟 Key Features

- **🔐 Secure Authentication**: Multi-user support with encrypted password hashing and session-based isolation.
- **🧠 Empathetic AI**: Powered by Google Gemini 1.5 Flash for nuanced, supportive dialogue.
- **🎭 Emotion-Driven UI**: Real-time sentiment analysis that dynamically shifts the UI theme to match your mood.
- **📊 Mood Analytics**: Interactive dashboard with Chart.js to track emotional trends over 7 days.
- **🎙️ Seamless Voice**: Integrated Web Speech API for natural voice-to-text and text-to-voice interaction.
- **📝 Weekly Summaries**: AI-generated reports summarizing your emotional journey and progress.

## ⚙️ How It Works

1.  **Input**: Users interact via text or voice.
2.  **Emotion Processing**: Every message is analyzed using `vaderSentiment` and custom heuristics.
3.  **AI Orchestration**: Context-aware prompts are sent to Gemini to generate supportive responses.
4.  **Reactive UI**: Glassmorphic interface updates dynamically based on detected emotions (Happy, Sad, Neutral).
5.  **Persistence**: All interactions and mood scores are securely stored in a SQLite database.

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
├── app.py                     # Main FastAPI entry point
├── services/                  # AI, Sentiment, and DB services
├── dashboard/                 # Analytics & Mood summary logic
├── ui/                        # Templates (Jinja2) and Static assets
├── data/                      # SQLite database storage
├── voice/                     # Voice input/output handlers
└── utils/                     # Security & Utility helpers
```

---
***Disclaimer**: This AI is for companionship and emotional support only. It is NOT a replacement for professional medical advice, diagnosis, or treatment. If you are in a crisis, please contact local emergency services immediately.*

