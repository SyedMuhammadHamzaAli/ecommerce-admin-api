from fastapi import FastAPI
from app.routes import products, sales, inventory  

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["Products"]) #
app.include_router(sales.router, prefix="/sales", tags=["Sales"]) #
# app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"]) # 
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
