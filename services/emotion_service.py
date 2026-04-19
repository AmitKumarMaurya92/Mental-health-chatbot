"""
Emotion service for detecting specific emotional states.
"""
from services.sentiment_service import analyze_sentiment, get_sentiment_label

def detect_emotion(text):
    """
    Placeholder for more complex emotion detection.
    Currently maps sentiment to basic emotional states.
    """
    sentiment = analyze_sentiment(text)
    label = get_sentiment_label(sentiment['compound'])
    
    mapping = {
        "positive": "Happy/Content",
        "negative": "Sad/Stressed",
        "neutral": "Calm"
    }
    
    return {
        "sentiment": sentiment,
        "label": label,
        "emotion": mapping.get(label, "Neutral")
    }
