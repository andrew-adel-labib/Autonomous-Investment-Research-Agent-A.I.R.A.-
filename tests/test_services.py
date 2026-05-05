from app.services.analysis_service import run_full_analysis


def test_full_analysis():
    result = run_full_analysis("AAPL")

    assert "company" in result
    assert "thesis" in result
    assert "signal" in result
    assert "sources" in result
    assert isinstance(result["insights"], list)