from app.agents.planner import create_research_plan
from app.agents.researcher import gather_research
from app.agents.synthesizer import synthesize_analysis
from app.agents.reflector import reflect_on_analysis


def test_planner():
    plan = create_research_plan("AAPL")

    assert plan["ticker"] == "AAPL"
    assert "financial_metrics" in plan["required_data"]


def test_research_pipeline():
    plan = create_research_plan("AAPL")
    research = gather_research(plan)

    assert "financials" in research
    assert "news" in research
    assert "filings" in research
    assert "sentiment_score" in research


def test_synthesis():
    mock_data = {
        "financials": {
            "company": "Apple Inc.",
            "ticker": "AAPL",
            "pe_ratio": 28,
            "revenue_growth": 0.08
        },
        "news": [],
        "filings": {
            "risk_factors": ["Regulatory pressure"]
        },
        "sentiment_score": 0.3
    }

    result = synthesize_analysis(mock_data)

    assert result["signal"] in ["Bullish", "Bearish", "Neutral"]
    assert "thesis" in result
    assert isinstance(result["insights"], list)


def test_reflection():
    result = {
        "sources": ["Yahoo Finance"],
        "confidence": 0.9,
        "thesis": "Strong company"
    }

    reflected = reflect_on_analysis(result)

    assert reflected["confidence"] < 0.9