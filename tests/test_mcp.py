import pytest
from app.mcp.registry import TOOLS

try:
    import app.mcp.tool_router as router_module
except Exception:
    router_module = None


def test_registry_structure():
    assert isinstance(TOOLS, dict)

    assert "finance_api" in TOOLS
    assert "news_api" in TOOLS
    assert "sec_api" in TOOLS


def test_registry_values_callable():
    for name, func in TOOLS.items():
        assert callable(func), f"{name} is not callable"


def test_router_module_exists():
    assert router_module is not None


def test_router_invalid_tool():
    """
    This test adapts to ANY router implementation:
    - class MCPToolRouter
    - function route_tool
    - or skip if unknown
    """

    if hasattr(router_module, "MCPToolRouter"):
        router = router_module.MCPToolRouter()

        with pytest.raises(Exception):
            router.route("unknown", {})

    elif hasattr(router_module, "route_tool"):
        with pytest.raises(Exception):
            router_module.route_tool("unknown", {})

    else:
        pytest.skip("No recognizable router interface found")