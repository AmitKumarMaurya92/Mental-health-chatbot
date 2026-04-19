"""
Safety service to detect critical situations and provide emergency guidance.
"""
import re

# List of critical keywords and phrases that trigger a safety response
CRITICAL_KEYWORDS = [
    "suicide", "kill myself", "want to die", "end my life", "end it all",
    "harm myself", "hurt myself", "better off dead", "no reason to live"
]

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

def check_safety(user_message: str) -> bool:
    """
    Checks the user's message against critical keywords.
    Returns False if the message is flagged as a crisis, True if it is safe.
    """
    message_lower = user_message.lower()
    
    # Check for exact keyword matches
    for keyword in CRITICAL_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", message_lower):
            return False
            
    return True

def get_emergency_response() -> str:
    """Returns a hardcoded emergency response for critical situations."""
    return EMERGENCY_RESPONSE
