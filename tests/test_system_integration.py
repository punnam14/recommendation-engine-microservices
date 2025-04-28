import requests

# PRODUCT_API = "http://localhost:5001/products"
# RECOMMENDATION_API = "http://localhost:5002/recommendations"

PRODUCT_API = "https://qa.hottake.pro/products"
RECOMMENDATION_API = "https://qa.hottake.pro/recommendations"

def test_endpoints():
    assert requests.get(PRODUCT_API).status_code == 200

def test_recommendations_flow():
    products = requests.get(PRODUCT_API).json()
    payload = {
        "preferences": {"priceRange": "all", "categories": ["Electronics"], "brands": []},
        "browsing_history": ["prod002"],
        "all_products": products
    }
    res = requests.post(RECOMMENDATION_API, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert all("product" in r for r in data["recommendations"][:3])