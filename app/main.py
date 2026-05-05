from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import Base, init_db
from app.core.middleware import (
    global_exception_handler,
    aira_exception_handler
)
from app.core.exceptions import AIRAException
from app.core.logger import get_logger

from app.api.routes import router as main_router
from app.api.dashboard import router as dashboard_router
from app.monitoring.prometheus import router as prometheus_router

from app.models.job import AnalysisJob

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = init_db()
    Base.metadata.create_all(bind=engine)

    logger.info("Database initialized successfully")
    logger.info("AIRA application started")

    yield

    logger.info("AIRA application shutting down")


app = FastAPI(
    title="AIRA",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(main_router)
app.include_router(dashboard_router)
app.include_router(prometheus_router)


app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AIRAException, aira_exception_handler)


@app.get("/")
def root():
    return {
        "app": "AIRA",
        "status": "running"
    }