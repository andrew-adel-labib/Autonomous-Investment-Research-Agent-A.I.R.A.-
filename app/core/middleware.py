from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import get_logger
from app.core.exceptions import AIRAException

logger = get_logger()

async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )

async def aira_exception_handler(request: Request, exc: AIRAException):
    logger.error(f"AIRA error: {str(exc)}")

    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "detail": str(exc)
        }
    )