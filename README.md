# E-Commerce Admin API

This is a backend E-Commerce Admin API developed using FastAPI and PostgreSQL. It provides functionality for managing products, tracking inventory, analyzing sales performance, and generating revenue reports.

---

## 📁 Project Structure

app/
├── db/
│ ├── database.py # DB connection
│ ├── models.py # SQLAlchemy models
│
├── routes/
│ ├── products.py # Product registration & listing
│ ├── inventory.py # Inventory tracking
│ ├── sales.py # Sales analytics
│
├── main.py # FastAPI entry point
└── seed_db.py # Demo data seeding
