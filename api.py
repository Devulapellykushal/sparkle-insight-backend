# api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from hybrid_insight_engine import generate_combined_insights
from trends import plot_health_trends
import base64
from io import BytesIO

app = FastAPI()

# ✅ Replace with your actual deployed frontend URL
origins = [
    "https://cursor-56s5mhmuz-devulapellykushals-projects.vercel.app",
    "http://localhost:3000"  # Optional: for local testing
]

# ✅ CORS setup so frontend can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cursor-56s5mhmuz-devulapellykushals-projects.vercel.app",  # 🟢 Replace this with your actual frontend URL
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # Load CSV
        df = pd.read_csv(file.file)
        print("✅ CSV successfully loaded.")
        print("📊 Data preview:\n", df.head())

        # Generate insights
        insights = generate_combined_insights(df)
        print("✅ Insights generated.")

        # Generate plot and convert to base64
        fig = plot_health_trends(df)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        img_str = base64.b64encode(buf.getvalue()).decode()

        return {
            "insights": insights,
            "trend_image": img_str
        }
    except Exception as e:
        print("❌ Error during processing:", str(e))
        return {"error": str(e)}
