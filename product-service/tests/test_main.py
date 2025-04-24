from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_products_endpoint_responds():
    response = client.get("/products")
    assert response.status_code == 200

def test_products_structure():
    response = client.get("/products")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for product in data:
        for field in ["id", "name", "category", "price", "brand"]:
            assert field in product
