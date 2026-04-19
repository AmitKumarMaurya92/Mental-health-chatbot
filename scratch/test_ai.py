
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from services.ai_service import generate_response

try:
    print("Testing generate_response...")
    response = generate_response("Hello, how are you?", username="test_user")
    print(f"Response: {response}")
except Exception as e:
    import traceback
    traceback.print_exc()
