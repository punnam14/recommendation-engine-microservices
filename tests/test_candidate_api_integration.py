import requests
import pytest

PRODUCT_API = "http://localhost:5001/products"
RECOMMENDATION_API = "http://localhost:5002/recommendations"


def test_api_availability():
    res = requests.get(PRODUCT_API)
    assert res.status_code == 200


def test_products_endpoint_structure():
    res = requests.get(PRODUCT_API)
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    for product in data[:3]:
        for field in ["id", "name", "category", "price", "brand"]:
            assert field in product


def test_recommendations_endpoint_structure():
    payload = {
        "preferences": {"priceRange": "all", "categories": ["Electronics"], "brands": []},
        "browsing_history": ["prod002"],
        "all_products": [
            {"id": "prod002", "name": "Headphones", "category": "Electronics", "price": 199.99, "brand": "Brand2", "tags": [], "rating": 5, "inventory": 1}
        ]
    }
    res = requests.post(RECOMMENDATION_API, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "recommendations" in data and isinstance(data["recommendations"], list)


def test_recommendation_quality_basic():
    res = requests.get(PRODUCT_API)
    products = res.json()
    payload = {
        "preferences": {"priceRange": "all", "categories": ["Electronics"], "brands": []},
        "browsing_history": ["prod002"],
        "all_products": products
    }
    rec_res = requests.post(RECOMMENDATION_API, json=payload)
    data = rec_res.json()
    assert "recommendations" in data and len(data["recommendations"]) >= 3
    for rec in data["recommendations"][:3]:
        assert "product" in rec and "explanation" in rec


def test_prompt_engineering_adaptation():
    p1 = {"preferences": {"priceRange": "all", "categories": ["Electronics"], "brands": []}, "browsing_history": []}
    p2 = {"preferences": {"priceRange": "all", "categories": ["Home"], "brands": []}, "browsing_history": []}

    res1 = requests.post(RECOMMENDATION_API, json=p1)
    res2 = requests.post(RECOMMENDATION_API, json=p2)
    ids1 = {rec["product"]["id"] for rec in res1.json().get("recommendations", [])}
    ids2 = {rec["product"]["id"] for rec in res2.json().get("recommendations", [])}

    assert len(ids1.intersection(ids2)) < max(len(ids1), len(ids2)) / 2, "Too much overlap between different preference sets"