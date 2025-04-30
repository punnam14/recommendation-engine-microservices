import requests
import pytest

# PRODUCT_API = "http://localhost:5001/products"
# RECOMMENDATION_API = "http://localhost:5002/recommendations"

PRODUCT_API = "https://qa.hottake.pro/products"
RECOMMENDATION_API = "https://qa.hottake.pro/recommendations"

def retry_get(url, retries=5, delay=5):
    for attempt in range(retries):
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return res
            print(f"[Attempt {attempt + 1}] Status code: {res.status_code}")
        except Exception as e:
            print(f"[Attempt {attempt + 1}] Exception: {e}")
        time.sleep(delay)
    raise Exception(f"Failed to get valid response from {url} after {retries} attempts")

def test_api_availability():
    res = requests.get(PRODUCT_API)
    assert res.status_code == 200


def test_products_endpoint_structure():
    res = retry_get(PRODUCT_API)
    try:
        data = res.json()
    except Exception:
        print("Invalid JSON response from products endpoint:", res.text)
        raise
    assert isinstance(data, list), f"Expected list, got: {type(data)}"
    assert len(data) >= 3, "Less than 3 products returned"
    for product in data[:3]:
        for field in ["id", "name", "category", "price", "brand"]:
            assert field in product, f"Missing field '{field}' in product: {product}"


def test_recommendations_endpoint_structure():
    payload = {
        "preferences": {"priceRange": "all", "categories": ["Electronics"], "brands": []},
        "browsing_history": ["prod002"],
        "all_products": [
            {"id": "prod002", "name": "Headphones", "category": "Electronics", "price": 199.99, "brand": "Brand2", "tags": [], "rating": 5, "inventory": 1}
        ]
    }
    res = requests.post(RECOMMENDATION_API, json=payload)
    assert res.status_code == 200, f"Status code was {res.status_code}, body: {res.text}"
    try:
        data = res.json()
    except Exception:
        print("Invalid JSON response from recommendation endpoint:", res.text)
        raise
    assert "recommendations" in data and isinstance(data["recommendations"], list)


def test_recommendation_quality_basic():
    res = retry_get(PRODUCT_API)
    try:
        products = res.json()
    except Exception:
        print("Invalid JSON from products in recommendation quality test:", res.text)
        raise
    payload = {
        "preferences": {"priceRange": "all", "categories": ["Electronics"], "brands": []},
        "browsing_history": ["prod002"],
        "all_products": products
    }
    rec_res = requests.post(RECOMMENDATION_API, json=payload)
    assert rec_res.status_code == 200, f"Status code was {rec_res.status_code}, body: {rec_res.text}"
    try:
        data = rec_res.json()
    except Exception:
        print("Invalid JSON from recommendations:", rec_res.text)
        raise
    assert "recommendations" in data and len(data["recommendations"]) >= 3
    for rec in data["recommendations"][:3]:
        assert "product" in rec and "explanation" in rec