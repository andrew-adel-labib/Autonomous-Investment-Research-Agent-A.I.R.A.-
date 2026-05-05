from prometheus_client import Counter, Histogram, generate_latest
from fastapi import APIRouter, Response

router = APIRouter()

REQUEST_COUNT = Counter(
    "aira_requests_total",
    "Total number of API requests",
    ["endpoint"]
)

JOB_COMPLETED = Counter(
    "aira_jobs_completed_total",
    "Total completed analysis jobs"
)

ERROR_COUNT = Counter(
    "aira_errors_total",
    "Total number of errors",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "aira_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)


def track_request(endpoint: str):
    REQUEST_COUNT.labels(endpoint=endpoint).inc()


def track_job_completed():
    JOB_COMPLETED.inc()


def track_error(endpoint: str):
    ERROR_COUNT.labels(endpoint=endpoint).inc()


def track_latency(endpoint: str, duration: float):
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)


@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")