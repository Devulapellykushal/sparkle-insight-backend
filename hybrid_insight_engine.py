# hybrid_insight_engine.py placeholder
# hybrid_insight_engine.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings('ignore')

# 1. Load and preprocess data
def load_health_logs(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.sort_values('date', inplace=True)
    return df

# 2. Train ML model for mood prediction
def train_mood_model(df):
    le = LabelEncoder()
    df['mood_encoded'] = le.fit_transform(df['mood'])

    X = df[['sleep_hours', 'hydration_ml', 'steps']]
    y = df['mood_encoded']

    model = LogisticRegression()
    model.fit(X, y)
    return model, le

# 3. Rule-based hydration check
def analyze_hydration(df):
    low_hydration_days = df[df['hydration_ml'] < 2200]
    if len(low_hydration_days) >= 3:
        return "🚰 Your hydration has been low for 3 or more days. Increase water intake."
    return None

# 4. Rule-based sleep check
def analyze_sleep(df):
    low_sleep_days = df[df['sleep_hours'] < 6]
    if len(low_sleep_days) >= 3:
        return "😴 Your sleep has been below 6 hours for multiple days. Aim for 7–8 hours of rest."
    return None

# 5. Rule-based steps check
def analyze_steps(df):
    avg_steps = df['steps'].mean()
    if avg_steps < 5000:
        return f"🚶‍♂️ Your average steps ({int(avg_steps)}) are lower than the healthy range. Try to stay more active."
    return None

# 6. ML-based mood insight
def analyze_mood_with_ml(df, model, le):
    X = df[['sleep_hours', 'hydration_ml', 'steps']]
    df['predicted_mood'] = le.inverse_transform(model.predict(X))
    sad_days = df[df['predicted_mood'] == 'sad']
    if len(sad_days) >= 3:
        return "🧠 Mood patterns suggest fatigue or stress. Consider self-care, better sleep, and hydration."
    return None

# 7. Combined engine
def generate_combined_insights(df):
    insights = []

    model, le = train_mood_model(df)

    # Rule-based
    for fn in [analyze_hydration, analyze_sleep, analyze_steps]:
        msg = fn(df)
        if msg:
            insights.append(msg)

    # ML-based
    mood_msg = analyze_mood_with_ml(df, model, le)
    if mood_msg:
        insights.append(mood_msg)

    return insights

# 8. Main entry
if __name__ == "__main__":
    df = load_health_logs("data/mock_health_logs.csv")
    insights = generate_combined_insights(df)

    print("\n💡 Health Insights Summary:")
    for insight in insights:
        print(f"- {insight}")
