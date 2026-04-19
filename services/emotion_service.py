"""
Emotion service for detecting specific emotional states.
"""
from services.sentiment_service import analyze_sentiment, get_sentiment_label

def detect_emotion(text):
    """
    Detects specific emotional states for UI adjustments and suggestions.
    """
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["angry", "mad", "frustrated", "hate", "furious", "annoyed"]):
        emotion = "Angry"
    elif any(word in text_lower for word in ["sad", "depressed", "down", "cry", "hopeless", "miserable"]):
        emotion = "Sad"
    elif any(word in text_lower for word in ["happy", "great", "awesome", "good", "excited", "joy", "glad"]):
        emotion = "Happy"
    else:
        # Fallback to sentiment analysis
        sentiment = analyze_sentiment(text)
        label = get_sentiment_label(sentiment['compound'])
        if label == "positive":
            emotion = "Happy"
        elif label == "negative":
            emotion = "Sad"
        else:
            emotion = "Neutral"
            
    return {
        "emotion": emotion
    }
