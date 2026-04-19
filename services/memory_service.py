from services.db_service import load_history_db, save_message_db, clear_chat_history_db

def load_history():
    """Loads the last 20 messages from the SQLite database."""
    return load_history_db(limit=20)

def save_message(role, content):
    """Saves a message to the SQLite database."""
    save_message_db(role, content)

def clear_history():
    """Clears the chat history from the database."""
    clear_chat_history_db()
