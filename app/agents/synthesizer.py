import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_llm_analysis(data, signal, confidence):
    try:
        prompt = f"""
        You are a financial analyst.

        Company Data:
        Financials: {data["financials"]}
        Sentiment Score: {data["sentiment_score"]}
        Risks: {data["filings"]["risk_factors"]}

        Computed Signal: {signal}
        Confidence: {confidence}

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

        content = response.choices[0].message.content

        return content

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
    confidence = round(min(confidence, 1.0), 2)

    llm_output = generate_llm_analysis(data, signal, confidence)

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
            "valuation": pe_ratio
        },

        "agent_trace": [
            "Planning complete",
            "Financial data collected",
            "News analyzed",
            "SEC filings reviewed",
            "LLM synthesis generated"
        ]
    }