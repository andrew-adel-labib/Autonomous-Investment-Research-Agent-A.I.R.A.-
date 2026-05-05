from pydantic import BaseModel
from typing import List, Dict, Any

class AgentSteps(BaseModel):
    plan: str
    research_summary: str
    synthesis_reasoning: str
    reflection_notes: str

class AnalysisResponse(BaseModel):
    company: str
    ticker: str
    thesis: str
    signal: str
    confidence: float
    insights: List[str]
    risks: List[str]
    sources: List[str]
    steps: AgentSteps
    metadata: Dict[str, Any]