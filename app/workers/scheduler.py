import uuid
from app.core.celery_app import celery
from app.workers.tasks import run_analysis
from app.core.logger import get_logger

logger = get_logger()


@celery.task(name="app.workers.scheduler.daily_analysis")
def daily_analysis():
    tickers = ["AAPL", "TSLA", "MSFT"]

    logger.info("[SCHEDULER] Running daily analysis")

    for ticker in tickers:
        job_id = str(uuid.uuid4())

        logger.info(f"[SCHEDULER] Dispatching {ticker}")

        run_analysis.delay(job_id, ticker)