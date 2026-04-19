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
    
    # 0. Safety Check First
    if not check_safety(user_message):
        # We don't save emergency responses to standard history, but we could.
        return get_emergency_response()
        
    if not OPENAI_API_KEY:
        return "I'm currently running in offline mode. Please configure an API key to chat."
        
    # 1. Analyze sentiment
    sentiment_scores = analyze_sentiment(user_message)
    sentiment_label = get_sentiment_label(sentiment_scores['compound'])
    
    # 2. Get a practical suggestion
    suggestion = get_suggestion_for_mood(sentiment_label)
    
    # 3. Build emotion-sensitive system prompt
    system_prompt = (
        "You are a gentle and supportive mental health companion. "
        f"The user's current emotional tone is detected as: {sentiment_label.upper()}. "
        "Adapt your response accordingly. If they are negative, be extra empathetic and comforting. "
        "If they are positive, be encouraging and happy for them. "
        f"Incorporate the following practical tip into your response naturally: '{suggestion}'"
    )
        
    # 4. Load Conversation Memory (keep it manageable, e.g., last 10 messages)
    history = load_history()[-10:]
    
    # 5. Build messages array
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    
    # Save the user's message to memory
    save_message("user", user_message)
        
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
        return f"I'm sorry, I encountered an error connecting to my brain: {str(e)}"




