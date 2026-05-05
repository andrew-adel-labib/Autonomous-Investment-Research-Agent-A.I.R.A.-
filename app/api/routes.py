import os
import json
import time
import app.core.database as db_module

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from sqlalchemy.orm import Session

from app.schemas.analysis import AnalyzeRequest, PortfolioRequest
from app.models.job import AnalysisJob
from app.workers.tasks import run_analysis
from app.reporting.json_formatter import format_pretty_json
from app.reporting.html_report import generate_html_report
from app.reporting.pdf_generator import generate_pdf
from app.agents.portfolio import compare_portfolio

from app.monitoring.prometheus import (
    track_request,
    track_latency,
    track_error
)

router = APIRouter()


def get_db():
    db = db_module.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_result(result):
    if isinstance(result, str):
        return json.loads(result)
    return result


@router.post("/analyze")
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    start = time.time()

    try:
        track_request("/analyze")

        job = AnalysisJob(
            ticker=request.ticker,
            status="queued"
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        if os.getenv("PYTEST_CURRENT_TEST") or os.getenv("ENVIRONMENT") == "test":
            run_analysis(str(job.id), request.ticker)
        else:
            run_analysis.delay(str(job.id), request.ticker)

        return {
            "job_id": str(job.id),
            "status": job.status
        }

    except Exception:
        track_error("/analyze")
        raise

    finally:
        track_latency("/analyze", time.time() - start)


@router.get("/status/{job_id}")
def get_status(job_id: str, db: Session = Depends(get_db)):
    start = time.time()

    try:
        track_request("/status")

        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return {
            "job_id": str(job.id),
            "status": job.status
        }

    except Exception:
        track_error("/status")
        raise

    finally:
        track_latency("/status", time.time() - start)


@router.get("/result/{job_id}")
def get_result(job_id: str, db: Session = Depends(get_db)):
    start = time.time()

    try:
        track_request("/result")

        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if job.status != "completed":
            return {
                "job_id": str(job.id),
                "status": job.status
            }

        result = parse_result(job.result)

        return {
            "job_id": str(job.id),
            "status": job.status,
            "result": result
        }

    except Exception:
        track_error("/result")
        raise

    finally:
        track_latency("/result", time.time() - start)


@router.get("/result/{job_id}/pretty")
def get_pretty_result(job_id: str, db: Session = Depends(get_db)):
    start = time.time()

    try:
        track_request("/result_pretty")

        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if job.status != "completed":
            return {"status": job.status}

        result = parse_result(job.result)
        pretty = format_pretty_json(result)

        return PlainTextResponse(pretty)

    except Exception:
        track_error("/result_pretty")
        raise

    finally:
        track_latency("/result_pretty", time.time() - start)


@router.get("/result/{job_id}/html", response_class=HTMLResponse)
def get_html_report(job_id: str, db: Session = Depends(get_db)):
    start = time.time()

    try:
        track_request("/result_html")

        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if job.status != "completed":
            return {"status": job.status}

        result = parse_result(job.result)
        html = generate_html_report(result)

        return HTMLResponse(content=html)

    except Exception:
        track_error("/result_html")
        raise

    finally:
        track_latency("/result_html", time.time() - start)


@router.get("/result/{job_id}/pdf")
def get_pdf_report(job_id: str, db: Session = Depends(get_db)):
    start = time.time()

    try:
        track_request("/result_pdf")

        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if job.status != "completed":
            return {"status": job.status}

        result = parse_result(job.result)
        file_path = generate_pdf(result, job_id)

        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=f"{job_id}.pdf"
        )

    except Exception:
        track_error("/result_pdf")
        raise

    finally:
        track_latency("/result_pdf", time.time() - start)


@router.post("/portfolio")
def portfolio_compare_endpoint(request: PortfolioRequest):
    start = time.time()

    try:
        track_request("/portfolio")

        if not request.reports:
            raise HTTPException(status_code=400, detail="Empty portfolio")

        return compare_portfolio(request.reports)

    except Exception:
        track_error("/portfolio")
        raise

    finally:
        track_latency("/portfolio", time.time() - start)


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total = db.query(AnalysisJob).count()
    completed = db.query(AnalysisJob).filter(AnalysisJob.status == "completed").count()
    failed = db.query(AnalysisJob).filter(AnalysisJob.status == "failed").count()

    latest_jobs = db.query(AnalysisJob)\
        .order_by(AnalysisJob.id.desc())\
        .limit(5)\
        .all()

    return {
        "total_jobs": total,
        "completed_jobs": completed,
        "failed_jobs": failed,
        "latest_jobs": [
            {"ticker": j.ticker, "status": j.status}
            for j in latest_jobs
        ]
    }


@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    jobs = db.query(AnalysisJob)\
        .filter(AnalysisJob.status == "completed")\
        .all()

    if not jobs:
        return {}

    confidences = []
    bullish = 0
    bearish = 0

    for job in jobs:
        result = parse_result(job.result)

        confidences.append(result.get("confidence", 0))

        if result.get("signal") == "Bullish":
            bullish += 1
        elif result.get("signal") == "Bearish":
            bearish += 1

    return {
        "avg_confidence": round(sum(confidences) / len(confidences), 3),
        "bullish": bullish,
        "bearish": bearish,
        "total": len(jobs)
    }