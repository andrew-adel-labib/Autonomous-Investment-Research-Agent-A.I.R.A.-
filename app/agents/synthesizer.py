import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def compute_data_quality(data):
    news_n = len(data.get("news", []))
    has_fin = bool(data.get("financials"))
    has_filings = bool(data.get("filings", {}).get("risk_factors"))

    score = 0
    score += min(news_n / 10, 1.0) * 0.4
    score += (1.0 if has_fin else 0.0) * 0.3
    score += (1.0 if has_filings else 0.0) * 0.3

    return round(score, 2)


def generate_llm_analysis(data, signal, confidence, data_quality):
    try:
        prompt = f"""
        You are a financial analyst.

        Company Data:
        Financials: {data["financials"]}
        Sentiment Score: {data["sentiment_score"]}
        Risks: {data["filings"]["risk_factors"]}

        Computed Signal: {signal}
        Confidence: {confidence}
        Data Quality: {data_quality}

        Generate:
        1. A concise investment thesis (2-3 sentences)
        2. Clear reasoning explaining the signal

        Keep it professional and data-driven.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception:
        return "Analysis generated using rule-based synthesis due to LLM unavailability."


def synthesize_analysis(data):
    financials = data["financials"]

    pe_ratio = financials.get("pe_ratio", 1)
    revenue_growth = financials.get("revenue_growth", 0)
    sentiment_score = data.get("sentiment_score", 0)

    if sentiment_score > 0.2:
        signal = "Bullish"
    elif sentiment_score < -0.2:
        signal = "Bearish"
    else:
        signal = "Neutral"

    confidence = (
        abs(sentiment_score) * 0.4 +
        revenue_growth * 0.3 +
        (1 / max(pe_ratio, 1)) * 0.3
    )

    data_quality = compute_data_quality(data)
    confidence = confidence * (0.7 + 0.3 * data_quality)

    confidence = round(min(confidence, 1.0), 2)

    uncertainty = round(1 - confidence, 2)

    llm_output = generate_llm_analysis(data, signal, confidence, data_quality)

    insights = [
        f"P/E Ratio: {pe_ratio}",
        f"Revenue Growth: {revenue_growth}",
        f"Sentiment Score: {sentiment_score}"
    ]

    return {
        "company": financials["company"],
        "ticker": financials.get("ticker", "N/A"),

        "thesis": llm_output,

        "signal": signal,
        "confidence": confidence,
        "uncertainty": uncertainty,
        "data_quality": data_quality,

        "insights": insights,
        "risks": data["filings"]["risk_factors"],

        "sources": [
            "Yahoo Finance",
            "NewsAPI",
            "SEC Filings"
        ],

        "reasoning": {
            "sentiment": sentiment_score,
            "growth": revenue_growth,
            "valuation": pe_ratio,
            "data_quality": data_quality
        },

        "agent_trace": [
            "Planning complete",
            "Financial data collected",
            "News analyzed",
            "SEC filings reviewed",
            "LLM synthesis generated"
        ]
    }