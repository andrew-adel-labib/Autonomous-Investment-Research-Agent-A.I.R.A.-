from app.mcp.client import MCPClient
from app.core.logger import get_logger

from transformers import pipeline

logger = get_logger()

try:
    sentiment_model = pipeline(
        "sentiment-analysis",
        model="ProsusAI/finbert"
    )
    logger.info("[RESEARCH] FinBERT model loaded")
except Exception as e:
    logger.warning(f"[RESEARCH] FinBERT failed to load: {e}")
    sentiment_model = None


def compute_sentiment(news):
    if not news:
        return 0.0

    if sentiment_model:
        scores = []

        for article in news:
            text = article.get("title", "")

            if not text:
                continue

            try:
                result = sentiment_model(text)[0]

                if result["label"] == "positive":
                    scores.append(1)
                elif result["label"] == "negative":
                    scores.append(-1)
                else:
                    scores.append(0)

            except Exception:
                continue

        return round(sum(scores) / max(len(scores), 1), 2)

    score = 0

    positive_words = ["growth", "profit", "strong", "beat", "upgrade"]
    negative_words = ["loss", "risk", "decline", "downgrade", "drop"]

    for article in news:
        title = article.get("title", "").lower()

        for w in positive_words:
            if w in title:
                score += 1

        for w in negative_words:
            if w in title:
                score -= 1

    return round(score / max(len(news), 1), 2)


def gather_research(plan):
    ticker = plan["ticker"]

    logger.info(f"[RESEARCH] Starting research for {ticker}")

    client = MCPClient()

    try:
        financials = client.call("finance_api", {"ticker": ticker})
        logger.info("[RESEARCH] Financial data fetched via MCP")
    except Exception as e:
        logger.warning(f"[RESEARCH] Financial API failed: {e}")

        financials = {
            "company": ticker,
            "pe_ratio": 20,
            "revenue_growth": 0.05
        }

    try:
        news = client.call("news_api", {"company": financials["company"]})
        logger.info(f"[RESEARCH] Retrieved {len(news)} news articles via MCP")
    except Exception as e:
        logger.warning(f"[RESEARCH] News API failed: {e}")
        news = []

    try:
        filings = client.call("sec_api", {"ticker": ticker})
        logger.info("[RESEARCH] SEC filings fetched via MCP")
    except Exception as e:
        logger.warning(f"[RESEARCH] SEC API failed: {e}")

        filings = {
            "risk_factors": ["Data unavailable"]
        }

    sentiment_score = compute_sentiment(news)

    logger.info(f"[RESEARCH] Sentiment score: {sentiment_score}")

    return {
        "financials": financials,
        "news": news,
        "filings": filings,
        "sentiment_score": sentiment_score
    }