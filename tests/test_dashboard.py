"""
tests/test_dashboard.py
=======================
Tests for the dashboard API endpoints.
"""

from fastapi.testclient import TestClient
from app.models.product import Product
from app.models.review import Review


def test_dashboard_overview(client: TestClient, db_session):
    """Test the /dashboard/overview endpoint."""
    # Seed data
    p1 = Product(name="Phone A", brand="Apple", price=1000, rating=4.5, review_count=100)
    p2 = Product(name="Phone B", brand="Samsung", price=800, rating=4.0, review_count=50)
    db_session.add_all([p1, p2])
    db_session.commit()

    r1 = Review(product_id=p1.id, review_text="Great phone", rating=5.0)
    r2 = Review(product_id=p2.id, review_text="Good but warm", rating=4.0)
    db_session.add_all([r1, r2])
    db_session.commit()

    response = client.get("/api/v1/dashboard/overview")
    assert response.status_code == 200
    data = response.json()["data"]
    
    assert data["total_products"] == 2
    assert data["total_reviews"] == 2
    assert data["average_rating"] == 4.25
    assert "overall_sentiment" in data


def test_dashboard_competitors(client: TestClient, db_session):
    """Test the /dashboard/competitors endpoint."""
    p1 = Product(name="Phone A", brand="Apple", price=1000, rating=4.5)
    p2 = Product(name="Phone B", brand="Apple", price=1200, rating=4.7)
    p3 = Product(name="Phone C", brand="Samsung", price=800, rating=4.0)
    db_session.add_all([p1, p2, p3])
    db_session.commit()

    response = client.get("/api/v1/dashboard/competitors")
    assert response.status_code == 200
    data = response.json()["data"]
    
    # We expect Apple and Samsung as brands
    assert len(data) == 2
    apple_data = next((item for item in data if item["brand"] == "Apple"), None)
    samsung_data = next((item for item in data if item["brand"] == "Samsung"), None)
    
    assert apple_data is not None
    assert apple_data["product_count"] == 2
    assert apple_data["avg_rating"] == 4.6
    
    assert samsung_data is not None
    assert samsung_data["product_count"] == 1
    assert samsung_data["avg_rating"] == 4.0
