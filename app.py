import sys
from fastapi import FastAPI, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import traceback
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from services.ai_service import generate_response
from services.memory_service import load_history, clear_history
from services.db_service import get_mood_history
from voice.input import listen_and_recognize
from voice.output import speak_text

app = FastAPI(title="Mental Health AI Companion")

# Enable sessions
app.add_middleware(SessionMiddleware, secret_key="secure_session_key_for_mental_health_companion")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"ERROR: Unhandled exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc), "traceback": traceback.format_exc()},
    )

# Setup templates and static files
app.mount("/static", StaticFiles(directory="ui/static"), name="static")
templates = Jinja2Templates(directory="ui/templates")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    sentiment: str = "neutral"

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_req: ChatRequest):
    """Basic text chatbot API endpoint."""
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not chat_req.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    reply = generate_response(chat_req.message, username=username)
    # Get emotion for UI
    from services.emotion_service import detect_emotion
    emotion = detect_emotion(chat_req.message)["emotion"].lower().split("/")[0]
    
    return ChatResponse(reply=reply, sentiment=emotion)

@app.post("/api/clear_chat")
async def clear_chat_endpoint(request: Request):
    """Clears the chat history."""
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Authentication required")
    clear_history(username=username)
    return {"status": "success"}

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    from services.db_service import get_user, create_user, verify_password
    
    user = get_user(username)
    if user:
        # User exists, check password
        if verify_password(password, user['password_hash']):
            request.session["user"] = username
            return RedirectResponse(url="/", status_code=303)
        else:
            # Invalid password
            return templates.TemplateResponse(request=request, name="login.html", context={"error": "Invalid password for this username. Please try again."})
    else:
        # New user, create account
        create_user(username, password)
        request.session["user"] = username
        return RedirectResponse(url="/", status_code=303)

@app.post("/delete_user")
async def delete_user(request: Request, username: str = Form(None)):
    current_user = request.session.get("user")
    
    # Use session user if form user is missing
    target_user = username or current_user
    
    if not current_user:
        print("DEBUG: Delete failed - No user in session")
        raise HTTPException(status_code=401, detail="Authentication required")
        
    if target_user != current_user:
        print(f"DEBUG: Delete failed - User '{current_user}' tried to delete '{target_user}'")
        raise HTTPException(status_code=403, detail="You can only delete your own account")
        
    print(f"DEBUG: Deleting user '{target_user}'")
    from services.db_service import delete_user_db, get_user
    
    if not get_user(target_user):
        print(f"DEBUG: Delete failed - User '{target_user}' not found in database")
        return RedirectResponse(url="/", status_code=303)
        
    try:
        delete_user_db(target_user)
        print(f"DEBUG: Successfully deleted user '{target_user}'")
    except Exception as e:
        print(f"DEBUG: Error deleting user '{target_user}': {e}")
        raise HTTPException(status_code=500, detail="Failed to delete account")
        
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def home_ui(request: Request):
    """Web UI Home Page."""
    username = request.session.get("user")
    if not username:
        return templates.TemplateResponse(request=request, name="login.html", context={})
    history = load_history(username=username)
    return templates.TemplateResponse(request=request, name="index.html", context={"history": history, "username": username})

@app.post("/chat_ui")
async def chat_ui_endpoint(request: Request, message: str = Form(...)):
    """Handles form submissions from the Web UI."""
    username = request.session.get("user")
    if not username:
        # Redirect to login if not an AJAX request
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return RedirectResponse(url="/", status_code=303)
        raise HTTPException(status_code=401, detail="Authentication required")
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
async def mood_trends(request: Request):
    """Returns mood data for the last 7 days."""
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Authentication required")
    history = get_mood_history(days=7, username=username)
    return {"history": history}

@app.get("/api/weekly_report")
async def weekly_report(request: Request):
    """Generates an AI summary of the user's emotional state."""
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Authentication required")
    from services.memory_service import load_history
    from dashboard.summary import generate_weekly_summary
    
    history = load_history(username=username)
    # Format history as text for the AI
    history_text = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in history[-20:]])
    
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
