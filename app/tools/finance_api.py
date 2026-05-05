import yfinance as yf
from app.core.logger import get_logger
from app.core.exceptions import DataSourceError

logger = get_logger()

def get_financial_data(ticker: str):
    try:
        logger.info(f"Fetching financial data for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info:
            raise DataSourceError(f"No financial data found for {ticker}")

        return {
            "company": info.get("longName"),
            "ticker": ticker,
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "revenue_growth": info.get("revenueGrowth"),
            "debt_to_equity": info.get("debtToEquity"),
            "profit_margin": info.get("profitMargins")
        }

    except Exception as e:
        logger.exception(f"Finance API failed for {ticker}: {str(e)}")
        raise DataSourceError(str(e))