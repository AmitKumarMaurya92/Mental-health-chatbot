import sys
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from services.ai_service import generate_response
from services.memory_service import load_history
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

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Basic text chatbot API endpoint."""
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    reply = generate_response(request.message)
    return ChatResponse(reply=reply)

@app.get("/", response_class=HTMLResponse)
async def home_ui(request: Request):
    """Web UI Home Page."""
    history = load_history()
    return templates.TemplateResponse(request=request, name="index.html", context={"history": history})

@app.post("/chat_ui", response_class=HTMLResponse)
async def chat_ui_endpoint(request: Request, message: str = Form(...)):
    """Handles form submissions from the Web UI."""
    reply = ""
    if message.strip():
        reply = generate_response(message)
    
    # Check if request is AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return {"reply": reply}
        
    # Redirect back to home to reload the updated history
    return RedirectResponse(url="/", status_code=303)

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

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        import uvicorn
        print("Starting web server... (Run with --cli for terminal mode)")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
