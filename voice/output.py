"""
Text to Speech module.
Converts text responses into spoken words.
"""
import pyttsx3

def speak_text(text):
    """Speaks the given text out loud."""
    if not text:
        return
        
    engine = pyttsx3.init()
    # Optional: configure voice properties
    # rate = engine.getProperty('rate')
    # engine.setProperty('rate', rate - 20)
    
    engine.say(text)
    engine.runAndWait()
