import sys
from fastapi import FastAPI, HTTPException, Request, Form, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from services.ai_service import generate_response
from services.memory_service import load_history, clear_history
from services.db_service import get_mood_history
from voice.input import listen_and_recognize
from voice.output import speak_text

app = FastAPI(title="Mental Health AI Companion")

# Setup templates and static files
app.mount("/static", StaticFiles(directory="ui/static"), name="static")
templates = Jinja2Templates(directory="ui/templates")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    sentiment: str = "neutral"

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, username: str = Cookie(default="default")):
    """Basic text chatbot API endpoint."""
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    reply = generate_response(request.message, username=username)
    # Get emotion for UI
    from services.emotion_service import detect_emotion
    emotion = detect_emotion(request.message)["emotion"].lower().split("/")[0]
    
    return ChatResponse(reply=reply, sentiment=emotion)

@app.post("/api/clear_chat")
async def clear_chat_endpoint(username: str = Cookie(default="default")):
    """Clears the chat history."""
    clear_history(username=username)
    return {"status": "success"}

@app.post("/login")
async def login(username: str = Form(...)):
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="username", value=username)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("username")
    return response

@app.get("/", response_class=HTMLResponse)
async def home_ui(request: Request, username: str = Cookie(default=None)):
    """Web UI Home Page."""
    from services.db_service import get_all_users
    users = get_all_users()
    if not username:
        return templates.TemplateResponse(request=request, name="login.html", context={"users": users})
    history = load_history(username=username)
    return templates.TemplateResponse(request=request, name="index.html", context={"history": history, "username": username, "users": users})

@app.post("/chat_ui")
async def chat_ui_endpoint(request: Request, message: str = Form(...), username: str = Cookie(default="default")):
    """Handles form submissions from the Web UI."""
    reply = ""
    sentiment = "neutral"
    if message.strip():
        reply = generate_response(message, username=username)
        from services.emotion_service import detect_emotion
        emotion = detect_emotion(message)["emotion"].lower().split("/")[0] # Gets happy, sad, or calm
        if emotion == "calm":
            emotion = "neutral"
        sentiment = emotion
    
    # Check if request is AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"reply": reply, "sentiment": sentiment})
        
    # Redirect back to home to reload the updated history
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/mood_trends")
async def mood_trends(username: str = Cookie(default="default")):
    """Returns mood data for the last 7 days."""
    history = get_mood_history(days=7, username=username)
    return {"history": history}

@app.get("/api/weekly_report")
async def weekly_report(username: str = Cookie(default="default")):
    """Generates an AI summary of the user's emotional state."""
    from services.memory_service import load_history
    from dashboard.summary import generate_weekly_summary
    
    history = load_history(username=username)
    # Format history as text for the AI
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-20:]])
    
    if not history_text.strip():
        summary = "Start chatting with me to get a weekly emotional summary!"
        improvement_text = "I don't have enough data yet to analyze your mood trends."
        return {"summary": summary, "improvement_text": improvement_text}
        
    summary = generate_weekly_summary(history_text)
    
    history_logs = get_mood_history(days=7, username=username)
    improvement_text = "Keep tracking your mood to see trends over time."
    if len(history_logs) >= 4:
        mid = len(history_logs) // 2
        first_half = sum(m['score'] for m in history_logs[:mid]) / mid
        second_half = sum(m['score'] for m in history_logs[mid:]) / (len(history_logs) - mid)
        if second_half > first_half:
            diff = min(100, int((second_half - first_half) * 50)) # simple calc
            improvement_text = f"Your mood improved by {diff}% this week! Keep it up."
        else:
            improvement_text = f"It seems you've had a tough time recently. Remember I'm here for you."
            
    return {"summary": summary, "improvement_text": improvement_text}

def run_cli(username="default"):
    """Runs the chatbot in an interactive CLI mode with voice support."""
    print(f"Welcome to your Mental Health AI Companion, {username}!")
    print("Type 'exit' to quit. Type 'voice' to toggle voice input.")
    
    use_voice = False
    
    while True:
        if use_voice:
            print("\nListening for your message...")
            user_input = listen_and_recognize()
            if not user_input:
                continue
        else:
            user_input = input("\nYou: ")
            
        if not user_input:
            continue
            
        if user_input.lower() == 'exit':
            print("Goodbye! Take care.")
            break
            
        if user_input.lower() == 'voice':
            use_voice = not use_voice
            status = "ON" if use_voice else "OFF"
            print(f"Voice mode is now {status}.")
            continue
            
        # Get AI response
        response = generate_response(user_input, username=username)
        print(f"\nAI: {response}")
        
        # Always speak if voice mode is on
        if use_voice:
            speak_text(response)

import threading
import schedule
import time

def run_scheduler():
    """Background task to run scheduled jobs."""
    while True:
        schedule.run_pending()
        time.sleep(1)

def daily_reminder():
    """Placeholder for a daily reminder action (e.g., logging or notification)."""
    print("⏰ [REMINDER] Time for your daily mental health check-in!")

# Schedule the reminder (e.g., every day at 10:00 AM)
schedule.every().day.at("10:00").do(daily_reminder)

if __name__ == "__main__":
    # Start scheduler thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    if "--cli" in sys.argv:
        cli_username = "default"
        for arg in sys.argv:
            if arg.startswith("--user="):
                cli_username = arg.split("=")[1]
        run_cli(cli_username)
    else:
        import uvicorn
        print("Starting web server... (Run with --cli for terminal mode)")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
# Trigger reload
