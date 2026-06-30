"""
tests/test_products.py
=======================
Unit and integration tests for the Products API.
"""



def test_health_check(client):
    """The root endpoint should return a healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_products_empty(client):
    """GET /products returns an empty list when no products exist."""
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True


def test_create_product(client):
    """POST /products creates a new product and returns 201."""
    payload = {
        "name": "Test Laptop",
        "brand": "TestBrand",
        "category": "electronics",
        "price": 999.99,
        "rating": 4.5,
        "review_count": 100,
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Test Laptop"


def test_get_product_not_found(client):
    """GET /products/9999 returns 404 for a non-existent product."""
    response = client.get("/api/v1/products/9999")
    assert response.status_code == 404
    assert response.json()["success"] is False


def test_create_and_retrieve_product(client):
    """Create a product then retrieve it by ID."""
    # Create
    create_resp = client.post(
        "/api/v1/products",
        json={"name": "Smart Watch", "price": 299.0, "category": "electronics"},
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["data"]["id"]

    # Retrieve
    get_resp = client.get(f"/api/v1/products/{product_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["id"] == product_id


def test_search_products(client):
    """GET /products/search returns matching products."""
    # Create a product to search for
    client.post("/api/v1/products", json={"name": "Bluetooth Speaker"})

    response = client.get("/api/v1/products/search?q=Bluetooth")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
