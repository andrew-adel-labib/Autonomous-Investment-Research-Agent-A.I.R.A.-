def create_research_plan(ticker: str):
    return {
        "ticker": ticker,
        "required_data": [
            "financial_metrics",
            "recent_news",
            "sec_filings"
        ]
    }