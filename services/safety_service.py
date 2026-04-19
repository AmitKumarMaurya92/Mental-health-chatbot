"""
Safety service to detect critical situations and provide emergency guidance.
"""
import re

# List of critical keywords and phrases that trigger a safety response
critical_words = ["suicide", "kill myself", "hopeless", "want to die", "end my life"]

EMERGENCY_RESPONSE = (
    "⚠️ I am so sorry you are feeling this way, but please know you are not alone. "
    "Your life has immense value. If you are in immediate danger or feeling overwhelmed "
    "by thoughts of suicide or self-harm, please reach out for help immediately.\n\n"
    "📞 **Emergency Contacts:**\n"
    "- National Suicide Prevention Lifeline: 988 (US)\n"
    "- Crisis Text Line: Text HOME to 741741\n"
    "- International resources: http://www.suicide.org/international-suicide-hotlines.html\n\n"
    "Please talk to someone who can support you right now."
)

def is_critical(text):
    """Checks if the user's message contains any critical keywords."""
    return any(word in text.lower() for word in critical_words)

def check_safety(user_message: str) -> bool:
    """Returns False if the message is critical, True otherwise."""
    return not is_critical(user_message)

def get_emergency_response() -> str:
    """Returns a hardcoded emergency response for critical situations."""
    return EMERGENCY_RESPONSE
