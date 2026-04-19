import matplotlib.pyplot as plt
import os
from utils.constants import DATA_DIR

def save_mood_plot(history):
    """Generates and saves a mood trend plot as an image."""
    if not history:
        return None
        
    dates = [h['timestamp'][:10] for h in history]
    scores = [h['score'] for h in history]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, scores, marker='o', linestyle='-', color='#8b5cf6')
    plt.title('Mood Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Mood Score (-1 to 1)')
    plt.grid(True, alpha=0.3)
    plt.ylim(-1, 1)
    
    plot_path = os.path.join(DATA_DIR, 'mood_trend.png')
    plt.savefig(plot_path)
    plt.close()
    return plot_path
