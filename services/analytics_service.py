"""
Analytics service for emotional trends and insights.
"""
from services.db_service import get_mood_history

def get_weekly_analytics():
    """Processes mood history for the last 7 days."""
    history = get_mood_history(days=7)
    if not history:
        return {"average_score": 0, "status": "No data"}
        
    scores = [h['score'] for h in history]
    labels = [h['label'] for h in history]
    
    avg_score = sum(scores) / len(scores)
    
    # Calculate most frequent emotion
    from collections import Counter
    most_common = Counter(labels).most_common(1)[0][0]
    
    status = "Stable"
    if avg_score > 0.5: status = "Very Positive"
    elif avg_score < -0.2: status = "Struggling"
    
    return {
        "average_score": round(avg_score, 2),
        "total_entries": len(history),
        "most_frequent_emotion": most_common,
        "status": status,
        "history": history
    }
