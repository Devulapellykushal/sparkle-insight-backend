# api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from hybrid_insight_engine import generate_combined_insights
from trends import plot_health_trends
import base64
from io import BytesIO

app = FastAPI()

# CORS setup so frontend can call this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    insights = generate_combined_insights(df)

    fig = plot_health_trends(df)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img_str = base64.b64encode(buf.getvalue()).decode()

    return {
        "insights": insights,
        "trend_image": img_str
    }
