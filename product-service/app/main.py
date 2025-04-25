from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .product_service import ProductService

app = FastAPI(title="Product Catalog Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

product_service = ProductService()

@app.get("/products")
async def get_products():
    return product_service.get_all_products()

# small change
