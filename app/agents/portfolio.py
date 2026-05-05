def compare_portfolio(reports: list):
    if not reports:
        return {"error": "Empty portfolio"}

    sorted_reports = sorted(
        reports,
        key=lambda x: x.confidence,
        reverse=True
    )

    best = sorted_reports[0]

    return {
        "best_stock": {
            "company": best.company,
            "ticker": best.ticker,
            "confidence": best.confidence
        },
        "ranking": [
            {
                "ticker": r.ticker,
                "confidence": r.confidence,
                "signal": r.signal
            }
            for r in sorted_reports
        ]
    }