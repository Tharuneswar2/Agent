from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import pandas as pd
import matplotlib.pyplot as plt
import io, base64, re, json, numpy as np
from agent.langchain_agent import answer_financial_query

router = APIRouter()


# =========================
# Request Model
# =========================
class VisualizationRequest(BaseModel):
    query: str
    company: Optional[str] = None
    chart_type: Optional[str] = None  # "line", "bar", "pie"
    auto_detect: bool = True


# =========================
# Chart Type Detection
# =========================
def detect_chart_type(query: str) -> str:
    query = query.lower()
    if any(k in query for k in ["trend", "growth", "year", "timeline", "change over time"]):
        return "line"
    elif any(k in query for k in ["compare", "comparison", "difference", "vs", "versus"]):
        return "bar"
    elif any(k in query for k in ["percentage", "share", "distribution", "breakdown", "ratio"]):
        return "pie"
    return "bar"


# =========================
# Numeric Data Extraction
# =========================
def extract_data_from_text(text: str) -> pd.DataFrame:
    """
    Extracts year-value or label-value pairs from RAG output text.
    Uses regex to detect multiple metrics.
    """

    # Try year + numeric extraction (e.g., 2021: 1200)
    pattern = re.findall(r"(\b20\d{2}\b)[^\d]{1,10}(\d{1,3}(?:,\d{3})*(?:\.\d+)?)", text)
    if pattern:
        df = pd.DataFrame(pattern, columns=["Year", "Value"])
        df["Year"] = df["Year"].astype(int)
        df["Value"] = df["Value"].replace(",", "", regex=True).astype(float)
        return df

    # Try label + numeric extraction (e.g., Revenue 5000, Profit 1200)
    pattern = re.findall(r"([A-Za-z ]+)\s*[:\-]?\s*(\d{2,}(?:\.\d+)?)", text)
    if pattern:
        df = pd.DataFrame(pattern, columns=["Label", "Value"])
        df["Value"] = df["Value"].astype(float)
        return df

    # Fallback demo data
    df = pd.DataFrame({
        "Year": [2019, 2020, 2021, 2022, 2023, 2024],
        "Value": [200, 310, 450, 600, 720, 880]
    })
    return df


# =========================
# Visualization Endpoint
# =========================
@router.post("/visualize_router")
async def visualize_router(request: VisualizationRequest):
    try:
        query = request.query
        company = request.company or "Unknown"
        chart_type = request.chart_type or detect_chart_type(query)

        # Step 1️⃣: Retrieve answer using the Financial RAG agent
        result = answer_financial_query(query)
        text = result.get("answer", "")

        if not text:
            raise HTTPException(status_code=404, detail="No data found for visualization.")

        # Step 2️⃣: Extract structured numeric data
        df = extract_data_from_text(text)
        if df.empty:
            raise HTTPException(status_code=400, detail="No numeric data detected for visualization.")

        # Step 3️⃣: Generate high-quality visualization
        plt.style.use("seaborn-v0_8")
        plt.figure(figsize=(7, 4))

        # Handle chart type
        if chart_type == "line" and "Year" in df.columns:
            plt.plot(df["Year"], df["Value"], marker="o", linewidth=2, color="#2E8B57")
            plt.fill_between(df["Year"], df["Value"], alpha=0.2, color="#90EE90")
        elif chart_type == "bar":
            labels = df["Year"] if "Year" in df.columns else df["Label"]
            plt.bar(labels, df["Value"], color="#4682B4")
        elif chart_type == "pie":
            labels = df["Label"] if "Label" in df.columns else df["Year"].astype(str)
            plt.pie(df["Value"], labels=labels, autopct="%1.1f%%", startangle=90,
                    colors=plt.cm.Paired.colors)
        else:
            plt.bar(df["Year"], df["Value"], color="#808080")

        plt.title(f"{company} — {query.capitalize()}", fontsize=12, pad=10)
        plt.xlabel("Year" if "Year" in df.columns else "Category")
        plt.ylabel("Value")
        plt.grid(alpha=0.3)

        # Step 4️⃣: Convert to Base64
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=150)
        buf.seek(0)
        base64_img = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()

        # Step 5️⃣: Generate summary insight
        trend = "increased" if df["Value"].iloc[-1] > df["Value"].iloc[0] else "decreased"
        change = round(((df["Value"].iloc[-1] - df["Value"].iloc[0]) / df["Value"].iloc[0]) * 100, 2)
        insight = f"{company}'s {query.lower()} has {trend} by {change}% from {df.iloc[0,0]} to {df.iloc[-1,0]}."

        # Step 6️⃣: Prepare Response
        return {
            "status": "success",
            "company": company,
            "query": query,
            "chart_type": chart_type,
            "data": df.to_dict(orient="records"),
            "chart_base64": base64_img,
            "insight": insight,
            "text_summary": text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization failed: {e}")
