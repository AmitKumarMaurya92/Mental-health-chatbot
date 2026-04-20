# MindMate AI ✨

**MindMate AI** is a premium, empathetic AI-powered mental health companion. Built with a focus on privacy, accessibility, and emotional intelligence, it provides a gentle, supportive space featuring emotion-sensitive responses, real-time safety checks, seamless voice interaction, and deep mood analytics.

![UI Screenshot](https://raw.githubusercontent.com/AmitKumarMaurya92/Mental-health-chatbot/main/ui/static/screenshot_mockup.png)

## 🌟 Key Features

### 🧠 Intelligence & Empathy
- **Empathetic AI Core**: Powered by **Google Gemini 1.5 Flash** for nuanced, supportive dialogue tailored to your emotional state.
- **Real-time Sentiment Analysis**: Every message is analyzed to understand your mood and adapt the conversation accordingly.
- **Weekly Progress Reports**: AI-generated insights that summarize your emotional journey and highlight growth patterns.

### 🎨 Immersive Experience
- **Emotion-Driven UI**: A stunning glassmorphic interface that dynamically shifts its theme (colors, gradients, and animations) to mirror your mood.
- **Seamless Voice Interaction**: Integrated STT (Speech-to-Text) and TTS (Text-to-Speech) for natural, hands-free support.
- **Responsive Mastery**: A fluid experience crafted for both desktop and mobile, ensuring support is always within reach.

### 🔐 Privacy & Security
- **Secure Isolation**: Robust multi-user authentication with encrypted password hashing (BCrypt) and session-based data scoping.
- **Data Sovereignty**: Permanent account deletion functionality—your data belongs to you, and you can wipe it at any time.
- **Local Persistence**: Mood logs and chat history are stored in a secure, locally-hosted SQLite database.

---

## ⚙️ Core Architecture

1.  **Sentiment Engine**: Uses `vaderSentiment` combined with custom heuristics to detect emotional nuances and intensity.
2.  **Contextual Orchestration**: Dynamically injects mood data and user history into Gemini's system instructions for highly personalized support.
3.  **Reactive Styling**: Uses a custom CSS variable system that updates in real-time based on the backend's emotional classification.
4.  **Safety First**: Multi-layer safety checks to detect crisis keywords and provide immediate emergency resources.

## 🛠️ Technology Stack

| Category | Technologies |
| :--- | :--- |
| **Backend Framework** | **FastAPI**, **Uvicorn**, Python 3.10+ |
| **AI Orchestration** | **Google Gemini 1.5 Flash** (`google-generativeai`), **Groq (Llama 3)** |
| **Emotional Intelligence** | **vaderSentiment** (Real-time scoring) |
| **Voice Processing** | **SpeechRecognition** (STT), **Pyttsx3** (TTS), **Web Speech API** |
| **Database & Auth** | **SQLite**, **SQLAlchemy**, **BCrypt** (Hashing), **Passlib** |
| **Frontend Interface** | **HTML5**, **CSS3 (Glassmorphism)**, **Jinja2** (Templating) |
| **Data Visualization** | **Chart.js** (Mood Trends), **Matplotlib** (Offline Analysis) |
| **Security & Session** | **ItsDangerous** (Signed Cookies), **Cryptography**, **Starlette** |
| **Infrastructure** | **Gunicorn** (Production), **Schedule** (Background Jobs) |

---

## 🚀 Setup & Installation

### **1. Prerequisites**
- Python 3.10 or higher
- Google AI Studio API Key ([Get it here](https://aistudio.google.com/))
- *Optional*: Groq API Key for faster fallback responses.

### **2. Local Installation**
```bash
# Clone the repository
git clone https://github.com/AmitKumarMaurya92/Mental-health-chatbot.git
cd mental-health-chatbot

# Set up virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Environment Configuration**
Create a `.env` file in the root directory:
```env
# Required
GEMINI_API_KEY_1=your_google_gemini_key

# Optional (for enhanced performance)
GROQ_API_KEY=your_groq_api_key
```

### **4. Launching the App**
```bash
python app.py
```
The application will be available at **`http://localhost:8000`**.

---

## 📂 Project Structure

```text
├── app.py                     # Main FastAPI application & route handlers
├── services/                  # Core logic: AI orchestration, sentiment, & DB
├── dashboard/                 # Analytics engines & automated summary generation
├── ui/                        # Frontend: Modern templates & dynamic CSS
│   ├── templates/             # Jinja2 HTML templates (index, login, dashboard)
│   └── static/                # CSS (themes, animations), JS, and assets
├── data/                      # Persistent SQLite database storage
├── voice/                     # Voice I/O: STT and TTS handlers
├── prompts/                   # Specialized AI instruction templates
├── tests/                     # Integrity and performance test suites
└── scratch/                   # Developer tools & database utilities
```

---

> [!IMPORTANT]
> **Disclaimer**: MindMate AI is designed for companionship and emotional support only. It is **not** a replacement for professional medical advice, diagnosis, or treatment. If you are in a crisis, please contact your local emergency services or a mental health professional immediately.

---
*Created with 🖤 for mental well-being.*
