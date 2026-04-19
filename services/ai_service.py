import openai
from config import OPENAI_API_KEY
from services.sentiment_service import analyze_sentiment, get_sentiment_label
from services.safety_service import check_safety, get_emergency_response
from services.suggestion_service import get_suggestion_for_mood

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def generate_response(user_message: str) -> str:
    """Sends a message to the AI API and returns the response, incorporating safety and sentiment analysis."""
    
    # 0. Safety Check First
    if not check_safety(user_message):
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
        
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"I'm sorry, I encountered an error connecting to my brain: {str(e)}"



