def get_sec_filings(ticker: str):
    return {
        "latest_10k": f"Mocked SEC filing summary for {ticker}",
        "risk_factors": [
            "Regulatory pressure",
            "Macroeconomic slowdown"
        ]
    }