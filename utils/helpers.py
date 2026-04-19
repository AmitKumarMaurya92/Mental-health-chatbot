"""
General helper functions.
"""
from datetime import datetime

def format_timestamp(ts_string):
    """Converts a timestamp string to a more readable format."""
    try:
        dt = datetime.fromisoformat(ts_string.replace('Z', '+00:00'))
        return dt.strftime("%b %d, %H:%M")
    except:
        return ts_string

def clean_text(text):
    """Basic text sanitization."""
    return text.strip()
