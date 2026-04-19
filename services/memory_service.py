"""
Memory service.
Stores and retrieves conversation history to provide context.
"""
import json
import os
from utils.constants import DATA_DIR

HISTORY_FILE = os.path.join(DATA_DIR, 'chat_history.json')

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_message(role, content):
    history = load_history()
    history.append({"role": role, "content": content})
    
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)
