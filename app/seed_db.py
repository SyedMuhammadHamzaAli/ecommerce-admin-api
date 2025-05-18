import sys
from datetime import datetime
from app.db.database import SessionLocal, engine
from app.db.models import Base, Product, Inventory, InventoryHistory, Sale
from faker import Faker
import random

fake = Faker()

def seed_data(force=False):
    db = SessionLocal()

    if force:
        db.query(Sale).delete()
        db.query(InventoryHistory).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.commit()
    else:
        if db.query(Product).first():
            print("⚠️ Data already exists. Skipping seeding.")
            db.close()
            return

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Predefined product names per category
    predefined_products = {
        "Electronics": ["Wireless Mouse", "Gaming Keyboard", "Smartphone", "Bluetooth Speaker", "PS5 Controller"],
        "Books": ["Atomic Habits", "The Great Gatsby", "Python Programming", "The Lean Startup", "1984"],
        "Toys": ["LEGO Set", "Remote Car", "Dollhouse", "Puzzle Box", "Action Figure"],
        "Home": ["Vacuum Cleaner", "Electric Kettle", "LED Lamp", "Coffee Maker", "Wall Clock"],
        "Fashion": ["Men's T-Shirt", "Women's Jacket", "Sneakers", "Leather Belt", "Sunglasses"]
    }

    products = []

    for category, names in predefined_products.items():
        for name in names:
            product = Product(
                name=name,
                category=category,
                price=round(random.uniform(10, 200), 2)
            )
            db.add(product)
            products.append(product)

    db.commit()

    for product in products:
        initial_stock = random.randint(0, 150)
        inventory = Inventory(
            product_id=product.id,
            stock=initial_stock,
            last_updated=datetime.utcnow()
        )
        db.add(inventory)
        db.flush()

        # Initial stock-in history
        history = InventoryHistory(
            inventory_id=inventory.id,
            old_stock=0,
            new_stock=initial_stock,
            change_date=inventory.last_updated
        )
        db.add(history)

        # Simulate 2–4 inventory changes
        for _ in range(random.randint(2, 4)):
            change = random.randint(-10, 20)
            old_stock = inventory.stock
            new_stock = max(0, old_stock + change)
            inventory.stock = new_stock
            inventory.last_updated = datetime.utcnow()

            history_entry = InventoryHistory(
                inventory_id=inventory.id,
                old_stock=old_stock,
                new_stock=new_stock,
                change_date=inventory.last_updated
            )
            db.add(history_entry)

        # Add fake sales data
        for _ in range(random.randint(5, 10)):
            sale = Sale(
                product_id=product.id,
                quantity=random.randint(1, 5),
                sale_date=fake.date_time_between(start_date='-30d', end_date='now')
            )
            db.add(sale)

    db.commit()
    db.close()
    print("✅ Database seeded with realistic product names and demo data.")

if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    seed_data(force=force_flag)




# from datetime import datetime
# from app.db.database import SessionLocal
# from app.db.models import Product, Inventory, Sale

# def seed_data():
#     db = SessionLocal()

#     if db.query(Product).first():
#         print("⚠️ Data already exists. Skipping seeding.")
#         return

#     # Create a product
#     product = Product(
#         name="Wireless Mouse",
#         category="Electronics",
#         price=29.99
#     )

#     # Create related inventory
#     inventory = Inventory(
#         product=product,
#         stock=100,
#         last_updated=datetime.utcnow()
#     )

#     # Create a sale
#     sale = Sale(
#         product=product,
#         quantity=5,
#         sale_date=datetime.utcnow()
#     )

#     db.add(product)
#     db.add(inventory)
#     db.add(sale)

#     db.commit()
#     db.close()

#     print("✅ Database seeded with sample data.")

# if __name__ == "__main__":
#     seed_data()
