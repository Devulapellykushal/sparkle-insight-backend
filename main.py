# main.py

from hybrid_insight_engine import load_health_logs, generate_combined_insights
from trends import plot_health_trends

def main():
    try:
        # 1. Load data
        file_path = "data/mock_health_logs.csv"
        df = load_health_logs(file_path)
        print("✅ Data loaded successfully.")

        # 2. Generate AI-based and rule-based insights
        print("\n💡 Personalized Health Insights:")
        insights = generate_combined_insights(df)
        for insight in insights:
            print(f"- {insight}")

        # 3. Visualize health trends
        print("\n📊 Displaying Health Trend Dashboard...")
        fig = plot_health_trends(df)
        fig.show()  # Or use plt.show() if needed

    except Exception as e:
        print(f"❌ Error in main flow: {e}")

if __name__ == "__main__":
    main()