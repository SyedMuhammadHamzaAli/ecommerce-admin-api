from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Sale, Product
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Get all or filtered sales
@router.get("/")
def get_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    product_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Sale).join(Product)

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if category:
        query = query.filter(Product.category == category)
    if product_id:
        query = query.filter(Sale.product_id == product_id)

    return query.all()

# 2. Revenue for a time period
@router.get("/revenue")
def get_revenue(
    period: str = Query("daily", enum=["daily", "weekly", "monthly", "annual"]),
    db: Session = Depends(get_db)
):
    now = datetime.now()
    period_map = {
        "daily": now - timedelta(days=1),
        "weekly": now - timedelta(weeks=1),
        "monthly": now - timedelta(days=30),
        "annual": now - timedelta(days=365),
    }

    start_date = period_map.get(period, now - timedelta(days=1))

    revenue = (
        db.query(func.sum(Sale.quantity * Product.price))
        .join(Product)
        .filter(Sale.sale_date >= start_date)
        .scalar()
    )

    return {"period": period, "revenue": revenue or 0}

# 3. Compare revenue between two date ranges
@router.get("/revenue/compare")
def compare_revenue(
    start_date_1: datetime,
    end_date_1: datetime,
    start_date_2: datetime,
    end_date_2: datetime,
    db: Session = Depends(get_db)
):
    rev1 = (
        db.query(func.sum(Sale.quantity * Product.price))
        .join(Product)
        .filter(Sale.sale_date >= start_date_1, Sale.sale_date <= end_date_1)
        .scalar()
    ) or 0

    rev2 = (
        db.query(func.sum(Sale.quantity * Product.price))
        .join(Product)
        .filter(Sale.sale_date >= start_date_2, Sale.sale_date <= end_date_2)
        .scalar()
    ) or 0

    return {
        "period_1": {"start": start_date_1, "end": end_date_1, "revenue": rev1},
        "period_2": {"start": start_date_2, "end": end_date_2, "revenue": rev2},
        "difference": rev2 - rev1
    }

# 4. Revenue by each category
@router.get("/revenue/by-category")
def revenue_by_category(
    db: Session = Depends(get_db)
):
    results = (
        db.query(Product.category, func.sum(Sale.quantity * Product.price).label("revenue"))
        .join(Product)
        .group_by(Product.category)
        .all()
    )

    return [{"category": r[0], "revenue": r[1]} for r in results]

@router.get("/summary")
def sales_summary(
    period: str = Query("daily", enum=["daily", "weekly", "monthly", "annual"]),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    product_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    # Adjust date truncation based on DB engine; assuming SQLite for now
    if period == "daily":
        group_func = func.date(Sale.sale_date)
    elif period == "weekly":
        group_func = func.strftime('%Y-%W', Sale.sale_date)
    elif period == "monthly":
        group_func = func.strftime('%Y-%m', Sale.sale_date)
    elif period == "annual":
        group_func = func.strftime('%Y', Sale.sale_date)
    else:
        raise HTTPException(status_code=400, detail="Invalid period")

    query = db.query(
        group_func.label("period"),
        func.sum(Sale.quantity).label("total_quantity"),
        func.sum(Sale.quantity * Product.price).label("total_revenue"),
    ).join(Product)

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if category:
        query = query.filter(Product.category == category)
    if product_id:
        query = query.filter(Sale.product_id == product_id)

    query = query.group_by("period").order_by("period")

    results = query.all()

    return [
        {
            "period": r.period,
            "total_quantity": r.total_quantity,
            "total_revenue": round(r.total_revenue, 2) if r.total_revenue else 0,
        }
        for r in results
    ]

@router.get("/best-sellers")
def best_sellers(
    top_n: int = 10,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            Product.id,
            Product.name,
            Product.category,
            func.sum(Sale.quantity).label("total_quantity"),
            func.sum(Sale.quantity * Product.price).label("total_revenue"),
        )
        .join(Sale)
        .group_by(Product.id)
    )

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if category:
        query = query.filter(Product.category == category)

    results = query.order_by(func.sum(Sale.quantity).desc()).limit(top_n).all()

    return [
        {
            "product_id": r.id,
            "name": r.name,
            "category": r.category,
            "total_quantity": r.total_quantity,
            "total_revenue": round(r.total_revenue, 2) if r.total_revenue else 0,
        }
        for r in results
    ]