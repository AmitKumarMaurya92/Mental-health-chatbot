import sys
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from services.ai_service import generate_response
from services.memory_service import load_history, clear_history
from services.db_service import get_mood_history
from services.journaling_service import analyze_and_save_journal, fetch_all_journals
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
async def chat_endpoint(request: ChatRequest):
    """Basic text chatbot API endpoint."""
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    reply = generate_response(request.message)
    # Get last mood log
    from services.db_service import get_mood_history
    history = get_mood_history(days=0) # Get today's logs
    sentiment = history[-1]["label"] if history else "neutral"
    
    return ChatResponse(reply=reply, sentiment=sentiment)

@app.post("/api/clear_chat")
async def clear_chat_endpoint():
    """Clears the chat history."""
    clear_history()
    return {"status": "success"}

@app.get("/", response_class=HTMLResponse)
async def home_ui(request: Request):
    """Web UI Home Page."""
    history = load_history()
    return templates.TemplateResponse(request=request, name="index.html", context={"history": history})

@app.post("/chat_ui")
async def chat_ui_endpoint(request: Request, message: str = Form(...)):
    """Handles form submissions from the Web UI."""
    reply = ""
    sentiment = "neutral"
    if message.strip():
        reply = generate_response(message)
        from services.db_service import get_mood_history
        history = get_mood_history(days=0)
        sentiment = history[-1]["label"] if history else "neutral"
    
    # Check if request is AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"reply": reply, "sentiment": sentiment})
        
    # Redirect back to home to reload the updated history
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/mood_trends")
async def mood_trends():
    """Returns mood data for the last 7 days."""
    history = get_mood_history(days=7)
    return {"history": history}

@app.get("/api/journals")
async def get_journals_api():
    """Returns all journal entries."""
    journals = fetch_all_journals()
    return {"journals": journals}

class JournalRequest(BaseModel):
    content: str
    title: str = "Daily Reflection"

@app.post("/api/save_journal")
async def save_journal_api(request: JournalRequest):
    """Saves a journal entry and returns AI feedback."""
    feedback = analyze_and_save_journal(request.content, title=request.title)
    return {"feedback": feedback}

def run_cli():
    """Runs the chatbot in an interactive CLI mode with voice support."""
    print("Welcome to your Mental Health AI Companion!")
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
        response = generate_response(user_input)
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
        run_cli()
    else:
        import uvicorn
        print("Starting web server... (Run with --cli for terminal mode)")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
# Trigger reload
