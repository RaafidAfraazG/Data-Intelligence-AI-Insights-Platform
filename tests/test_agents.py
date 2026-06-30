"""
tests/test_agents.py
====================
Tests for the AI Agent endpoints.
"""

from fastapi.testclient import TestClient


def test_trigger_collect_agent(client: TestClient, db_session, monkeypatch):
    """Test that the data collector agent can be triggered."""
    # We don't want to actually run Playwright or BS4 in tests, so we mock the agent.
    class MockDataCollector:
        def __init__(self, db):
            self.db = db
            
        def run(self, urls, csv_path, scraper_type):
            return {
                "urls_scraped": 0,
                "csv_imported": 1,
                "raw_items": 10,
                "cleaned_items": 9,
                "summary": "Mock summary"
            }
            
    # Mock the endpoint's dependency or the class itself.
    import app.api.routes.agents as agents_module
    monkeypatch.setattr(agents_module, "DataCollectorAgent", MockDataCollector)
    
    response = client.post(
        "/api/v1/agents/collect", 
        json={"urls": [], "csv_path": "mock.csv", "scraper_type": "beautifulsoup"}
    )
    
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["csv_imported"] == 1
    assert data["cleaned_items"] == 9
