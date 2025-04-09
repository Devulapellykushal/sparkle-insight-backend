# trends.py

import pandas as pd
import matplotlib.pyplot as plt

# Optional for better visuals
plt.style.use('ggplot')

# Load CSV and preprocess
def load_health_logs(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.sort_values('date', inplace=True)

    # Map mood text to numeric
    mood_map = {'sad': 0, 'neutral': 1, 'happy': 2}
    df['mood_score'] = df['mood'].map(mood_map)

    return df

# Generate health trend figure (return fig, not show here)
def plot_health_trends(df):
    mood_map = {'sad': 0, 'neutral': 1, 'happy': 2}
    df['mood_score'] = df['mood'].map(mood_map)
    dates = df['date']

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    axs[0, 0].plot(dates, df['sleep_hours'], marker='o')
    axs[0, 0].set_title('Sleep Duration (hrs)')
    axs[0, 0].set_xlabel('Date')
    axs[0, 0].set_ylabel('Hours')

    axs[0, 1].plot(dates, df['mood_score'], marker='o', color='orange')
    axs[0, 1].set_title('Mood Score (0=Sad, 1=Neutral, 2=Happy)')
    axs[0, 1].set_xlabel('Date')
    axs[0, 1].set_ylabel('Mood Score')

    axs[1, 0].plot(dates, df['hydration_ml'], marker='o', color='blue')
    axs[1, 0].set_title('Hydration (ml)')
    axs[1, 0].set_xlabel('Date')
    axs[1, 0].set_ylabel('ml')

    axs[1, 1].plot(dates, df['steps'], marker='o', color='green')
    axs[1, 1].set_title('Steps Count')
    axs[1, 1].set_xlabel('Date')
    axs[1, 1].set_ylabel('Steps')

    plt.tight_layout()
    return fig  # ⬅️ return the figure instead of showing

# Local test
if __name__ == "__main__":
    df = load_health_logs("data/mock_health_logs.csv")
    fig = plot_health_trends(df)
    fig.show()  # Show only during direct execution
