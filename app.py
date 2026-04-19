import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.ai_service import generate_response
from voice.input import listen_and_recognize
from voice.output import speak_text

app = FastAPI(title="Mental Health AI Companion")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Basic text chatbot endpoint."""
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    reply = generate_response(request.message)
    return ChatResponse(reply=reply)

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
        
        # Always speak if voice mode is on, or maybe always speak in CLI? 
        # Let's speak if voice mode is on.
        if use_voice:
            speak_text(response)

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        import uvicorn
        print("Starting web server... (Run with --cli for terminal mode)")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
