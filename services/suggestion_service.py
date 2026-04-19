"""
Suggestion service for providing mental health tips and coping strategies.
"""
import random

BREATHING_EXERCISES = [
    "Try the 4-7-8 breathing technique: Breathe in for 4 seconds, hold for 7 seconds, and exhale slowly for 8 seconds.",
    "Try Box Breathing: Inhale for 4 seconds, hold for 4 seconds, exhale for 4 seconds, and hold for 4 seconds. Repeat this a few times.",
    "Take a deep breath in through your nose, let your belly fill with air, and gently exhale through your mouth."
]

GROUNDING_TECHNIQUES = [
    "Try the 5-4-3-2-1 technique: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
    "Focus on your feet. Feel them resting on the floor. Notice the pressure, the temperature, and the connection to the ground.",
    "Grab an object near you. Focus entirely on its texture, temperature, and weight in your hand."
]

def get_suggestion_for_mood(sentiment_label: str) -> str:
    """Returns a gentle suggestion based on the detected sentiment."""
    if sentiment_label == "negative":
        # Offer a grounding or breathing exercise when they are down
        tips = BREATHING_EXERCISES + GROUNDING_TECHNIQUES
        return random.choice(tips)
    elif sentiment_label == "positive":
        return "Keep focusing on what's going well! Maybe write down one thing you're grateful for today."
    else:
        # Neutral
        return "Remember to take breaks and stay hydrated today."
