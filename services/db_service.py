"""
Database service using SQLite for persistent storage.
Handles chat history, journal entries, and mood tracking.
"""
import sqlite3
import os
from datetime import datetime
from utils.constants import DATA_DIR

DB_PATH = os.path.join(DATA_DIR, 'companion.db')

def init_db():
    """Initializes the database tables if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Messages table for chat history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT DEFAULT 'default',
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Journals table for personal reflections
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT DEFAULT 'default',
            title TEXT,
            content TEXT NOT NULL,
            mood_tag TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Mood logs for tracking trends
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT DEFAULT 'default',
            score REAL NOT NULL,
            label TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Migrations for existing DB
    for table in ['messages', 'journals', 'mood_logs']:
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN username TEXT DEFAULT 'default'")
        except sqlite3.OperationalError:
            pass # Column already exists
    
    conn.commit()
    conn.close()

def save_message_db(role, content, username="default"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (username, role, content) VALUES (?, ?, ?)', (username, role, content))
    conn.commit()
    conn.close()

def clear_chat_history_db(username="default"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def load_history_db(limit=20, username="default"):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT role, content, timestamp FROM messages WHERE username = ? ORDER BY timestamp DESC LIMIT ?', (username, limit))
    rows = cursor.fetchall()
    conn.close()
    
    # Return in chronological order
    history = [{"role": row["role"], "content": row["content"], "timestamp": row["timestamp"]} for row in rows]
    return history[::-1]

def save_journal(content, title=None, mood_tag=None, username="default"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO journals (username, title, content, mood_tag) VALUES (?, ?, ?, ?)', (username, title, content, mood_tag))
    conn.commit()
    conn.close()

def get_journals(username="default"):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content, mood_tag, timestamp FROM journals WHERE username = ? ORDER BY timestamp DESC', (username,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def log_mood(score, label, username="default"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mood_logs (username, score, label) VALUES (?, ?, ?)', (username, score, label))
    conn.commit()
    conn.close()

def get_mood_history(days=7, username="default"):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT score, label, timestamp 
        FROM mood_logs 
        WHERE username = ? AND timestamp >= date('now', ?) 
        ORDER BY timestamp ASC
    ''', (username, f'-{days} days'))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Get distinct usernames from all tables to be safe
    cursor.execute('''
        SELECT DISTINCT username FROM messages
        UNION
        SELECT DISTINCT username FROM mood_logs
        UNION
        SELECT DISTINCT username FROM journals
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows if row[0] and row[0] != 'default']

# Initialize on import
init_db()
