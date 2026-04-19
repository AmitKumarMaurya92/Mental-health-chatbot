"""
Module for generating weekly summaries.
"""
from services.ai_service import get_gemini_model

def generate_weekly_summary(history_text):
    """Uses Gemini to summarize the week's emotional state."""
    system_prompt = "You are a helpful mental health analyst. Summarize the user's emotional week based on these messages."
    model = get_gemini_model(system_instruction=system_prompt)
    
    if not model:
        return "Summary unavailable in offline mode."
        
    try:
        response = model.generate_content(f"History: {history_text}")
        return response.text.strip()
    except Exception:
        return "Could not generate summary at this time."
