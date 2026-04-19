"""
Daily Check-in CLI Script.
This script can be run daily to prompt the user for a quick mood check-in.
The results are saved to the chatbot's memory.
"""
import sys
import os

# Add the project root to sys.path to import services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import generate_response
from services.memory_service import save_message
from services.sentiment_service import analyze_sentiment, get_sentiment_label
from voice.output import speak_text

def run_checkin():
    print("\n" + "="*40)
    print("🌟 DAILY MENTAL HEALTH CHECK-IN 🌟")
    print("="*40 + "\n")
    
    greeting = "Hello! I'm your AI Companion. How are you feeling today? (Type your response or 'exit' to quit)"
    print(f"AI: {greeting}")
    speak_text(greeting)
    
    user_input = input("\nYou: ").strip()
    
    if not user_input or user_input.lower() == 'exit':
        print("Okay, no problem. Have a wonderful day!")
        return

    # Analyze mood immediately
    sentiment = analyze_sentiment(user_input)
    mood = get_sentiment_label(sentiment['compound'])
    
    # Save to memory as a specific check-in event
    checkin_msg = f"[DAILY CHECK-IN] User is feeling {mood.upper()}. Content: {user_input}"
    save_message("user", checkin_msg)
    
    # Generate an empathetic response
    response = generate_response(user_input)
    
    print(f"\nAI: {response}")
    speak_text(response)
    
    print("\n" + "="*40)
    print("Check-in complete. Take care of yourself today!")
    print("="*40 + "\n")

if __name__ == "__main__":
    run_checkin()
