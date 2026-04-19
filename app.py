from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.ai_service import generate_response

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
