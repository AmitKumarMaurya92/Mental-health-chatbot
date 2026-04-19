"""
Global constants for the application.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Default API setup (OpenAI or Gemini)
AI_PROVIDER = "openai" # Change to "gemini" if needed

# Safety thresholds
VADER_NEGATIVE_THRESHOLD = -0.5
