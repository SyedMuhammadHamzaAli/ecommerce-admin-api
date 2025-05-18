from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Inventory, InventoryHistory
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

LOW_STOCK_THRESHOLD_DEFAULT = 10

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class InventoryBase(BaseModel):
    product_id: int
    stock: int

class InventoryResponse(InventoryBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True

class InventoryHistoryResponse(BaseModel):
    id: int
    old_stock: int
    new_stock: int
    change_date: datetime

    class Config:
        orm_mode = True

# Get All Inventory Items with Pagination
@router.get("/", response_model=list[InventoryResponse])
def get_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).offset(skip).limit(limit).all()
    return inventory

# Get Low Stock Items with Pagination
@router.get("/low-stock", response_model=list[InventoryResponse])
def get_low_stock_products(
    threshold: int = Query(LOW_STOCK_THRESHOLD_DEFAULT, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db)
):
    low_stock = (
        db.query(Inventory)
        .filter(Inventory.stock < threshold)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return low_stock

# Update Inventory & Log History
@router.put("/update", response_model=InventoryResponse)
def update_inventory(update: InventoryBase, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(Inventory.product_id == update.product_id).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    old_stock = inventory_item.stock
    inventory_item.stock = update.stock
    inventory_item.last_updated = datetime.utcnow()

    # Record history
    history_record = InventoryHistory(
        inventory_id=inventory_item.id,
        old_stock=old_stock,
        new_stock=update.stock,
        change_date=datetime.utcnow()
    )
    db.add(history_record)
    db.commit()
    db.refresh(inventory_item)

    return inventory_item

# Get Inventory History with Pagination
@router.get("/{product_id}/history", response_model=list[InventoryHistoryResponse])
def get_inventory_history(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db)
):
    inventory_item = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    history = (
        db.query(InventoryHistory)
        .filter(InventoryHistory.inventory_id == inventory_item.id)
        .order_by(InventoryHistory.change_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return history

