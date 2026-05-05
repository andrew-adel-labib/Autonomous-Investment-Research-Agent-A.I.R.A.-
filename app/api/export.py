from fastapi import APIRouter
from app.reporting.json_formatter import format_pretty_json
from app.reporting.html_report import generate_html_report

router = APIRouter()

@router.post("/export/json")
def export_json(data: dict):
    return format_pretty_json(data)

@router.post("/export/html")
def export_html(data: dict):
    return generate_html_report(data)