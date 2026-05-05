from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    ticker: str

class AnalyzeResponse(BaseModel):
    job_id: str
    status: str

class FinalAnalysis(BaseModel):
    company: str
    ticker: str
    thesis: str
    signal: str
    confidence: float
    insights: List[str]
    risks: List[str]
    sources: List[str]
    agent_trace: List[str]
    
class Report(BaseModel):
    company: str
    ticker: str
    signal: str
    confidence: float

class PortfolioRequest(BaseModel):
    reports: List[Report]