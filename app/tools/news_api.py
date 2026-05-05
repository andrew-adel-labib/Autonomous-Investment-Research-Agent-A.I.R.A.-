import httpx
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import DataSourceError

logger = get_logger()

def get_company_news(company: str):
    try:
        logger.info(f"Fetching news for {company}")
        url = f"https://newsapi.org/v2/everything?q={company}&apiKey={settings.NEWS_API_KEY}"
        response = httpx.get(url, timeout=15)
        response.raise_for_status()

        articles = response.json().get("articles", [])

        return [
            {
                "title": a["title"],
                "source": a["source"]["name"],
                "url": a["url"]
            }
            for a in articles[:5]
        ]

    except Exception as e:
        logger.exception(f"News API failed for {company}: {str(e)}")
        raise DataSourceError(str(e))