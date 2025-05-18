# 🛒 E-Commerce Admin API

This is a backend **E-Commerce Admin API** developed using **FastAPI** and **PostgreSQL**. It provides functionality for managing products, tracking inventory, analyzing sales performance, and generating revenue reports.

---

## 📁 Project Structure

```text
app/
├── db/
│   ├── database.py       # DB connection
│   └── models.py         # SQLAlchemy models
│
├── routes/
│   ├── products.py       # Product registration & listing
│   ├── inventory.py      # Inventory tracking
│   └── sales.py          # Sales analytics
│
├── main.py               # FastAPI entry point
└── seed_db.py            # Demo data seeding
```

## 🛠 Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/SyedMuhammadHamzaAli/ecommerce-admin-api.git
cd ecommerce-admin-api
```
2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the FastAPI app:

```
uvicorn app.main:app --reload
```
