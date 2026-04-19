"""
Text to Speech module.
Converts text responses into spoken words.
"""
try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    HAS_TTS = False

def speak_text(text):
    """Speaks the given text out loud."""
    if not text or not HAS_TTS:
        return
        
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[WARN] TTS failed: {e}")
