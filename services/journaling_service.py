"""
Journal service for analyzing personal reflections.
Uses Gemini to provide empathetic feedback on journal entries.
"""
from services.ai_service import get_gemini_model
from services.db_service import save_journal, get_journals

def analyze_and_save_journal(content, title=None):
    """Analyzes a journal entry with AI and saves it to the database."""
    
    # 1. Use Gemini to provide a brief empathetic reflection on the entry
    system_prompt = (
        "You are a gentle and insightful journaling assistant. "
        "Your task is to read a user's journal entry and provide a single paragraph of "
        "warm, empathetic feedback. Highlight their strengths and offer a comforting perspective."
    )
    
    model = get_gemini_model(system_instruction=system_prompt)
    feedback = "Thank you for sharing your thoughts today. Taking time to reflect is a wonderful step for your well-being."
    
    if model:
        try:
            response = model.generate_content(f"Journal Entry: {content}")
            feedback = response.text.strip()
        except Exception:
            pass
            
    # 2. Identify a 'mood tag' (simple approach for now)
    # We could use sentiment analysis here too
    from services.sentiment_service import analyze_sentiment, get_sentiment_label
    scores = analyze_sentiment(content)
    mood_tag = get_sentiment_label(scores['compound'])
    
    # 3. Save to DB
    save_journal(content, title=title, mood_tag=mood_tag)
    
    return feedback

def fetch_all_journals():
    return get_journals()
