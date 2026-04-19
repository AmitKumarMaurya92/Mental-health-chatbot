import openai
from config import OPENAI_API_KEY
from services.sentiment_service import analyze_sentiment, get_sentiment_label
from services.safety_service import check_safety, get_emergency_response
from services.suggestion_service import get_suggestion_for_mood
from services.memory_service import load_history, save_message

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def generate_response(user_message: str) -> str:
    """Sends a message to the AI API and returns the response, incorporating memory, safety and sentiment analysis."""
    
    # 0. Save the user's message to memory immediately
    # This ensures that even if something fails later, the user's input is logged.
    save_message("user", user_message)

    # 1. Safety Check
    if not check_safety(user_message):
        reply = get_emergency_response()
        save_message("assistant", reply)
        return reply
        
    if not OPENAI_API_KEY:
        # Mock responses for offline mode to keep the experience interactive
        mock_responses = [
            "I'm currently in offline mode (API key missing), but I'm still here to listen. How else can I support you?",
            "I'm resting my AI brain right now, but feel free to keep sharing your thoughts with me.",
            "I've received your message! Without my full connection, I can't give a detailed reply, but I'm here for you.",
            "I'm listening. Sometimes just putting things into words can help, even if I'm offline."
        ]
        import random
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
    # We load history which now includes the user message we just saved
    history = load_history()[-10:]
    
    # 6. Build messages array
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        ai_reply = response.choices[0].message.content.strip()
        
        # Save the AI's reply to memory
        save_message("assistant", ai_reply)
        
        return ai_reply
    except Exception as e:
        reply = f"I'm sorry, I encountered an error connecting to my brain: {str(e)}"
        save_message("assistant", reply)
        return reply




