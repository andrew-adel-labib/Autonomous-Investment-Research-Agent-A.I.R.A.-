from app.agents.planner import create_research_plan
from app.agents.researcher import gather_research
from app.agents.synthesizer import synthesize_analysis
from app.agents.reflector import reflect_on_analysis
from app.agents.trend_analyzer import analyze_trend
from app.core.logger import get_logger
from app.core.exceptions import AgentExecutionError
from app.core.cache import get_cached, set_cache

logger = get_logger()


def run_full_analysis(ticker: str):
    try:
        logger.info(f"[ANALYSIS] Starting analysis for {ticker}")

        cache_key = f"analysis:{ticker}"

        cached = get_cached(cache_key)
        if cached:
            logger.info(f"[CACHE] Returning cached result for {ticker}")
            return cached

        plan = create_research_plan(ticker)
        logger.info("[ANALYSIS] Research plan created")

        research = gather_research(plan)
        logger.info("[ANALYSIS] Research gathered")

        synthesis = synthesize_analysis(research)
        logger.info("[ANALYSIS] Synthesis complete")

        final_result = reflect_on_analysis(synthesis)
        logger.info("[ANALYSIS] Reflection complete")

        price_series = [100, 102, 105, 110]
        trend = analyze_trend(price_series)
        final_result["trend"] = trend

        final_result["steps"] = {
            "plan": str(plan),
            "research_summary": f"Collected financials, news, filings for {ticker}",
            "synthesis_reasoning": final_result.get("reasoning", ""),
            "reflection_notes": final_result.get("reflection_notes", [])
        }

        set_cache(cache_key, final_result)
        logger.info(f"[CACHE] Stored result for {ticker}")

        logger.info(f"[ANALYSIS] Completed for {ticker}")
        return final_result

    except Exception as e:
        logger.exception(f"[ANALYSIS] Failed for {ticker}: {str(e)}")
        raise AgentExecutionError(str(e))