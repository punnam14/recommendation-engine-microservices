from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recommendation_endpoint_structure():
    payload = {
        "preferences": {
            "priceRange": "all",
            "categories": ["Electronics"],
            "brands": []
        },
        "browsing_history": ["prod002"],
        "all_products": [{
            "id": "prod002",
            "name": "Test Headphones",
            "category": "Electronics",
            "price": 199.99,
            "brand": "TestBrand",
            "tags": [],
            "rating": 5,
            "inventory": 1
        }]
    }
    response = client.post("/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)