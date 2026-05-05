from fastapi import APIRouter
from app.monitoring.metrics import collect_metrics

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    return {
        "status": "running",
        "metrics": collect_metrics()
    }