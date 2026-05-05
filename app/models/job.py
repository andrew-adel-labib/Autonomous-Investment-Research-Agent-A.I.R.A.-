from sqlalchemy import Column, String, JSON, DateTime
from datetime import datetime
from app.core.database import Base
import uuid

class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticker = Column(String, nullable=False)
    status = Column(String, default="queued")
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)