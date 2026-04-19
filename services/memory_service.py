from services.db_service import load_history_db, save_message_db, clear_chat_history_db

def load_history(username="default"):
    """Loads the last 20 messages from the SQLite database."""
    return load_history_db(limit=20, username=username)

def save_message(role, content, username="default"):
    """Saves a message to the SQLite database."""
    save_message_db(role, content, username=username)

def clear_history(username="default"):
    """Clears the chat history from the database."""
    clear_chat_history_db(username=username)
