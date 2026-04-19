"""
Module for generating weekly summaries.
"""
from services.ai_service import get_gemini_model, groq_client

def generate_weekly_summary(history_text):
    """Uses Gemini (or Groq fallback) to summarize the week's emotional state."""
    system_prompt = (
        "You are an AI Weekly Report Generator for a mental health companion app. "
        "Analyze the provided conversation history and generate a short, insightful summary. "
        "Format your response with the following 3 short sections using markdown: "
        "\n\n**📈 Mood Trends:**\n(Summarize how their mood has been)"
        "\n\n**💡 Suggestions:**\n(Provide 1-2 actionable tips)"
        "\n\n**⭐ Progress:**\n(Highlight something positive or encouraging)"
    )
    
    # 1. Try Groq first (usually faster and more reliable fallback)
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"History: {history_text}"}
                ],
                temperature=0.5
            )
            text = response.choices[0].message.content.strip()
            return format_summary_html(text)
        except Exception as e:
            print(f"[WARN] Groq summary failed: {e}. Trying Gemini.")

    # 2. Try Gemini
    model = get_gemini_model(system_instruction=system_prompt)
    if model:
        try:
            response = model.generate_content(f"History: {history_text}")
            return format_summary_html(response.text.strip())
        except Exception:
            pass
            
    return "Summary unavailable at this time. Please try again later."

def format_summary_html(text):
    """Converts simple markdown bolding and newlines to HTML."""
    import re
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = text.replace('\n', '<br>')
    return text

