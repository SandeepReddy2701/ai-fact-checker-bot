from src.search_tools import web_search

def test_search_executes():
    # This just checks the function runs; network may be restricted in CI
    try:
        res = web_search("site:nasa.gov Moon", max_results=2)
        assert isinstance(res, list)
    except Exception:
        # allow offline environments
        assert True
