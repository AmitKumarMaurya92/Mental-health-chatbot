import sqlite3
import os
from services.db_service import init_db, create_user, get_user, delete_user_db

def test_delete():
    init_db()
    username = "test_deletion_script"
    password = "password123"
    
    print(f"Creating user {username}...")
    create_user(username, password)
    
    user = get_user(username)
    if user:
        print(f"User {username} created successfully.")
    else:
        print(f"Failed to create user {username}.")
        return

    print(f"Deleting user {username}...")
    delete_user_db(username)
    
    user = get_user(username)
    if not user:
        print(f"User {username} deleted successfully.")
    else:
        print(f"Failed to delete user {username}.")

if __name__ == "__main__":
    test_delete()
