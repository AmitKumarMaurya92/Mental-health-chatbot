# AI Voice-Based Mental Health Companion ✨

An empathetic, AI-powered mental health companion built with **Python**, **FastAPI**, and **Google Gemini 1.5 Flash**. This companion provides a gentle, supportive space with emotion-sensitive responses, real-time safety checks, seamless voice interaction, and persistent mood tracking.

![UI Screenshot](file:///C:/Users/amitk/.gemini/antigravity/brain/84d49de7-72cb-4e7d-b0da-e563e70d8466/verified_ui_changes_1776612157489.png)

## ⚙️ How It Works

The application operates through a seamless pipeline designed for empathy and responsiveness:

1.  **Input**: Users interact via text or voice (using Browser Speech API).
2.  **Emotion Processing**: Every message is analyzed in real-time using `vaderSentiment` and custom emotion detection services to identify the user's mood.
3.  **AI Orchestration**: The message, along with conversation history and sentiment data, is sent to **Google Gemini 1.5 Flash**. The AI is instructed to respond as a supportive mental health companion.
4.  **Reactive UI**: The frontend receives the response and the detected emotion, triggering a dynamic CSS theme shift (e.g., calming blues for neutral, vibrant greens for happy, or warm oranges for sadness).
5.  **Analytics & Memory**: Responses and mood scores are persisted in a **SQLite** database. A background scheduler also runs to manage daily reminders and weekly summary generation.

## 🛠️ Technology Used

### **Backend**
- **Python 3.10+**: Core logic.
- **FastAPI**: High-performance web framework for APIs and routing.
- **Google Generative AI**: Gemini 1.5 Flash for empathetic dialogue.
- **VADER Sentiment**: For real-time emotional analysis.
- **SQLite**: Lightweight persistent storage.
- **Schedule**: For background mental health check-ins.

### **Frontend**
- **HTML5 & CSS3**: Custom glassmorphic design system.
- **Vanilla JavaScript**: Real-time UI updates and AJAX communication.
- **Jinja2**: Server-side templating.
- **Chart.js**: Interactive mood visualization dashboard.

### **Voice & Media**
- **Web Speech API**: Browser-based speech-to-text.
- **SpeechRecognition & pyttsx3**: Backend fallback for CLI mode.

## 🚀 Setup & Installation

Follow these steps to get your companion up and running locally:

### **1. Prerequisites**
- Python 3.10 or higher installed.
- A Google AI Studio API Key (Get it from [aistudio.google.com](https://aistudio.google.com/)).

### **2. Clone the Repository**
```bash
git clone https://github.com/AmitKumarMaurya92/Mental-health-chatbot.git
cd mental-health-chatbot
```

### **3. Environment Setup**
Create a virtual environment and install dependencies:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### **4. Configuration**
Create a `.env` file in the root directory and add your API keys:
```env
GEMINI_API_KEY_1=your_gemini_api_key_here
```

### **5. Run the Application**
```bash
python app.py
```
The application will be available at `http://localhost:8000`.

## 🎮 Usage

- **Web Mode**: Simply open `http://localhost:8000` in your browser.
- **CLI Mode**: Run `python app.py --cli` to interact directly in your terminal.
- **Voice Mode**: Click the microphone icon in the web UI or type `voice` in CLI mode to toggle voice interactions.

## 📁 Project Structure
```text
mental-health-voice-chatbot/
├── app.py                     # Main entry point & FastAPI setup
├── services/                  # AI, Sentiment, and DB services
├── dashboard/                 # Analytics & Mood summary logic
├── ui/                        # Templates (Jinja2) and Static assets (CSS/JS)
├── data/                      # SQLite database files
├── voice/                     # Voice input/output handlers
└── utils/                     # Utility functions
```

---
***Disclaimer**: This AI is for companionship and emotional support only. It is NOT a replacement for professional medical advice, diagnosis, or treatment. If you are in a crisis, please contact local emergency services or a mental health professional immediately.*
