
import requests

# Start a session
session = requests.Session()

# 1. Login (or at least hit the home page to get a session if needed, but here we need to login)
# Since I don't know a valid user, I'll try to login as 'test_user' / 'password'
# If it doesn't exist, it creates it.
print("Logging in...")
login_response = session.post("http://localhost:8000/login", data={"username": "test_user", "password": "password"}, allow_redirects=True)
print(f"Login status: {login_response.status_code}")

# 2. Send chat message
print("Sending chat message...")
chat_response = session.post(
    "http://localhost:8000/chat_ui", 
    data={"message": "I am feeling a bit stressed today."},
    headers={"X-Requested-With": "XMLHttpRequest"}
)

print(f"Chat status: {chat_response.status_code}")
try:
    print(f"Chat response: {chat_response.json()}")
except:
    print(f"Chat response text: {chat_response.text}")
