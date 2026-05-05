from app.tools.finance_api import get_financial_data
from app.tools.news_api import get_company_news
from app.tools.sec_api import get_sec_filings

TOOLS = {
    "finance_api": get_financial_data,
    "news_api": get_company_news,
    "sec_api": get_sec_filings,
}