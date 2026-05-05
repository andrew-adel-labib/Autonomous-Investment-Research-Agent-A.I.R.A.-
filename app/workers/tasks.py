import json
import time
import app.core.database as db_module

from app.core.celery_app import celery
from app.services.analysis_service import run_full_analysis
from app.models.job import AnalysisJob
from app.core.database import init_db
from app.core.logger import get_logger

from app.monitoring.prometheus import (
    track_request,
    track_job_completed,
    track_error,
    track_latency
)

logger = get_logger()


@celery.task(
    name="app.workers.tasks.run_analysis",
    bind=True,
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True
)
def run_analysis(self, job_id: str, ticker: str):
    start = time.time()

    init_db()
    db = db_module.SessionLocal()
    job = None

    try:
        track_request("celery_task")

        job = db.query(AnalysisJob).filter(
            AnalysisJob.id == job_id
        ).first()

        if not job:
            logger.error(f"[TASK] Job {job_id} not found")
            return

        if job.status in ["running", "completed"]:
            logger.warning(f"[TASK] Job {job_id} already processed")
            return

        logger.info(f"[TASK] Starting job {job_id} for {ticker}")

        job.status = "running"
        db.commit()

        result = run_full_analysis(ticker)

        try:
            serialized_result = json.dumps(result)
        except Exception as e:
            logger.error(f"[TASK] Serialization failed: {e}")
            raise

        logger.info(f"[TASK] Result ready for job {job_id}")

        job.status = "completed"
        job.result = serialized_result
        db.commit()

        track_job_completed()

        logger.info(f"[TASK] Job {job_id} completed successfully")

    except Exception as e:
        logger.exception(f"[TASK] Job {job_id} failed: {str(e)}")

        track_error("celery_task")

        if job:
            job.status = "failed"
            job.result = json.dumps({
                "error": str(e),
                "job_id": job_id
            })
            db.commit()

        raise e

    finally:
        duration = time.time() - start
        track_latency("celery_task", duration)

        db.close()