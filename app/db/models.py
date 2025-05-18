from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, index=True)
    price = Column(Float, nullable=False)

    sales = relationship("Sale", back_populates="product")
    inventory = relationship("Inventory", back_populates="product", uselist=False)


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    sale_date = Column(DateTime, nullable=False)

    product = relationship("Product", back_populates="sales")


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    stock = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    product = relationship("Product", back_populates="inventory")
    history = relationship("InventoryHistory", back_populates="inventory", cascade="all, delete-orphan")

class InventoryHistory(Base):
    __tablename__ = 'inventory_history'
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    old_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)
    change_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    inventory = relationship("Inventory", back_populates="history")