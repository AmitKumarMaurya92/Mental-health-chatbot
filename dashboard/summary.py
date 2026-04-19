"""
Module for generating weekly summaries.
"""
from services.ai_service import get_gemini_model

def generate_weekly_summary(history_text):
    """Uses Gemini to summarize the week's emotional state."""
    system_prompt = (
        "You are an AI Weekly Report Generator for a mental health companion app. "
        "Analyze the provided conversation history and generate a short, insightful summary. "
        "Format your response with the following 3 short sections using markdown: "
        "\n\n**📈 Mood Trends:**\n(Summarize how their mood has been)"
        "\n\n**💡 Suggestions:**\n(Provide 1-2 actionable tips)"
        "\n\n**⭐ Progress:**\n(Highlight something positive or encouraging)"
    )
    model = get_gemini_model(system_instruction=system_prompt)
    
    if not model:
        return "Summary unavailable in offline mode."
        
    try:
        response = model.generate_content(f"History: {history_text}")
        # Convert simple markdown to HTML using simple string replace for the UI
        text = response.text.strip()
        import re
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = text.replace('\n', '<br>')
        return text
    except Exception:
        return "Could not generate summary at this time."
