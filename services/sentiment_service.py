from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of a given text.
    Returns a dictionary with 'pos', 'neu', 'neg', and 'compound' scores.
    """
    return analyzer.polarity_scores(text)

def get_sentiment_label(compound_score: float) -> str:
    """
    Converts a compound score into a human-readable label.
    """
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"
