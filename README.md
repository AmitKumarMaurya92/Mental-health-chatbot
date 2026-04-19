# AI Voice-Based Mental Health Companion ✨

An empathetic, AI-powered mental health companion built with **Python**, **FastAPI**, and **Google Gemini 1.5 Flash**. This companion provides a gentle, supportive space with emotion-sensitive responses, real-time safety checks, seamless voice interaction, and persistent mood tracking.

![UI Mockup](https://raw.githubusercontent.com/AmitKumarMaurya92/Mental-health-chatbot/main/docs/ui_mockup.png)

## ✨ Phase 1: Core Essentials (Must-Have)
- **Empathetic Conversations**: Powered by Google Gemini with custom system instructions.
- **Sentiment Analysis**: Real-time mood detection using VADER.
- **Voice-Enabled**: Integrated Speech-to-Text (STT) and Text-to-Speech (TTS).
- **Safety First**: Immediate crisis detection and emergency resource guidance.
- **Suggestions**: Mood-based activities and coping strategies.

## 🚀 Phase 2: Strong Features (Persistence & Insights)
- **SQLite Persistence**: Robust database storage for chats, journals, and mood logs.
- **AI Journaling Assistant**: Write reflections and receive warm, AI-powered feedback.
- **Mood Dashboard**: Interactive **Chart.js** graphs to visualize your emotional journey.
- **Weekly Analytics**: Automatic calculation of average mood and frequent emotions.
- **Memory Context**: AI remembers your history to provide personalized support.

## 💎 Phase 3: Premium Features (Reactive UI)
- **Emotion-Based UI Morphing**: The interface colors change dynamically based on your mood (e.g., Sad → Red, Happy → Green).
- **Dark/Light Mode**: Seamless theme switching with persistent preferences.
- **Advanced Dashboard**: Modular analytics with Matplotlib Fallback for static reporting.
- **Scheduled Check-ins**: Background scheduler for daily mental health reminders.

## 🛠️ Project Structure
```text
mental-health-voice-chatbot/
├── app.py                     # Main application & Scheduler
├── services/                  # AI, Safety, Sentiment, Journaling, Analytics
├── dashboard/                 # Mood plotting & Weekly summaries
├── voice/                     # CLI Voice input/output
├── data/                      # SQLite DB, logs, and generated charts
├── ui/                        # Glassmorphic templates and themes
└── utils/                     # Helper functions and constants
```

## 🚀 Quick Start

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/AmitKumarMaurya92/Mental-health-chatbot.git
   cd mental-health-chatbot
   pip install -r requirements.txt
   ```
2. **Configure**: Add `GEMINI_API_KEY_1` to your `.env` file.
3. **Run**:
   ```bash
   python app.py
   ```

---
*Disclaimer: This AI is for companionship only and is not a replacement for professional medical help.*
