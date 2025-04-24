import pytest
from app.llm_service import LLMService

sample_products = [
    {"id": "prod001", "name": "Test Shoe", "category": "Footwear", "price": 89.99, "brand": "TestBrand", "tags": ["running", "lightweight"], "rating": 4.5, "inventory": 10},
    {"id": "prod002", "name": "Test Headphones", "category": "Electronics", "price": 199.99, "brand": "TestSound", "tags": ["audio", "wireless"], "rating": 4.9, "inventory": 5},
    {"id": "prod003", "name": "Eco Bottle", "category": "Home", "price": 29.99, "brand": "EcoBrand", "tags": ["reusable", "hydration"], "rating": 4.6, "inventory": 50},
    {"id": "prod004", "name": "Reusable Kitchen Towels", "category": "Home", "price": 19.99, "brand": "EcoBrand", "tags": ["reusable", "kitchen", "eco-friendly"], "rating": 4.4, "inventory": 30},
]


def test_filter_products_for_llm_logic():
    llm = LLMService()
    user_prefs = {
        "priceRange": "under50",
        "categories": ["Home"],
        "brands": []
    }
    browsing = [sample_products[2]]  # Eco Bottle
    result = llm._filter_products_for_llm(user_prefs, browsing, sample_products)

    assert result, "Expected filtered products but got empty list"
    assert all(p["price"] <= 50 for p in result), "Some products exceed price cap"


def test_get_products_by_tags():
    llm = LLMService()
    result = llm._get_products_by_tags(["wireless"], sample_products, 200, exclude_ids=set())
    assert len(result) == 1 and result[0]["id"] == "prod002", "Expected Test Headphones"


def test_get_related_tags_from_llm():
    llm = LLMService()
    tags = llm._get_related_tags_from_llm(["hydration"], {"hydration", "eco", "wireless", "kitchen"})
    assert isinstance(tags, list), "Tags must be a list"
    assert all(isinstance(tag, str) for tag in tags), "Tags must be strings"