import google.generativeai as genai
from config import GEMINI_API_KEYS
from services.sentiment_service import analyze_sentiment, get_sentiment_label
from services.safety_service import check_safety, get_emergency_response
from services.suggestion_service import get_suggestion_for_mood
from services.memory_service import load_history, save_message
import random

# Initialize Gemini with the first available key
def get_gemini_model():
    for key in GEMINI_API_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            return model
        except Exception:
            continue
    return None

model = get_gemini_model()

def generate_response(user_message: str) -> str:
    """Sends a message to the Gemini API and returns the response, incorporating memory, safety and sentiment analysis."""
    
    # 0. Save the user's message to memory immediately
    save_message("user", user_message)

    # 1. Safety Check
    if not check_safety(user_message):
        reply = get_emergency_response()
        save_message("assistant", reply)
        return reply
        
    if not model:
        # Mock responses for offline mode
        mock_responses = [
            "I'm currently in offline mode (API key missing), but I'm still here to listen. How else can I support you?",
            "I'm resting my AI brain right now, but feel free to keep sharing your thoughts with me.",
            "I've received your message! Without my full connection, I can't give a detailed reply, but I'm here for you.",
            "I'm listening. Sometimes just putting things into words can help, even if I'm offline."
        ]
        reply = random.choice(mock_responses)
        save_message("assistant", reply)
        return reply
        
    # 2. Analyze sentiment
    sentiment_scores = analyze_sentiment(user_message)
    sentiment_label = get_sentiment_label(sentiment_scores['compound'])
    
    # 3. Get a practical suggestion
    suggestion = get_suggestion_for_mood(sentiment_label)
    
    # 4. Build emotion-sensitive system prompt
    system_prompt = (
        "You are a gentle and supportive mental health companion. "
        f"The user's current emotional tone is detected as: {sentiment_label.upper()}. "
        "Adapt your response accordingly. If they are negative, be extra empathetic and comforting. "
        "If they are positive, be encouraging and happy for them. "
        f"Incorporate the following practical tip into your response naturally: '{suggestion}'"
    )
        
    # 5. Load Conversation Memory (keep it manageable, e.g., last 10 messages)
    history = load_history()[-10:]
    
    # 6. Convert history to Gemini format
    # Gemini uses 'user' and 'model'
    chat_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        chat_history.append({"role": role, "parts": [msg["content"]]})
    
    try:
        # Start a chat session with history
        chat = model.start_chat(history=chat_history[:-1]) # History except the last user message
        
        # Prepend system prompt instructions to the current message or use it to guide the model
        # Gemini 1.5 doesn't have a direct 'system' role in the same way as OpenAI in the start_chat history easily without specific config
        # But we can use system_instruction in the model constructor or just prepend it.
        # Let's use the current user message but include the system prompt context.
        
        full_user_input = f"[CONTEXT: {system_prompt}]\n\nUser Message: {user_message}"
        
        response = chat.send_message(full_user_input)
        ai_reply = response.text.strip()
        
        # Save the AI's reply to memory
        save_message("assistant", ai_reply)
        
        return ai_reply
    except Exception as e:
        reply = f"I'm sorry, I encountered an error connecting to my brain: {str(e)}"
        save_message("assistant", reply)
        return reply
