from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Product
from pydantic import BaseModel

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for product input
class ProductCreate(BaseModel):
    name: str
    category: str
    price: float

# GET: Fetch all products
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# POST: Register new product
@router.post("/register")
def register_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {
        "message": "✅ Product registered successfully",
        "product": {
            "id": db_product.id,
            "name": db_product.name,
            "category": db_product.category,
            "price": db_product.price
        }
    }
