from app.mcp.registry import TOOLS
from app.core.logger import get_logger
import time

logger = get_logger()


def call_tool(name: str, params: dict, retries: int = 2):
    """
    Central MCP tool executor

    Features:
    - Logging (start/end)
    - Retry mechanism
    - Execution timing
    - Safe error handling
    """

    tool = TOOLS.get(name)

    if not tool:
        raise ValueError(f"[MCP] Tool '{name}' not found")

    for attempt in range(retries + 1):
        try:
            start_time = time.time()

            logger.info(f"[MCP] → Calling '{name}' with params={params}")

            result = tool(**params)

            duration = round(time.time() - start_time, 3)

            logger.info(f"[MCP] ← '{name}' completed in {duration}s")

            return result

        except Exception as e:
            logger.warning(
                f"[MCP] '{name}' failed (attempt {attempt + 1}/{retries + 1}): {str(e)}"
            )

            if attempt == retries:
                logger.error(f"[MCP] '{name}' failed after all retries")
                raise