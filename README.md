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

### API will be accessible at: http://127.0.0.1:8000
### Swagger UI docs: /docs

## 🗂 API Endpoints

## 🧾 Products

| Method | Endpoint              | Description                    |
|--------|------------------------|--------------------------------|
| GET    | `/products/`           | Fetch all registered products. |
| POST   | `/products/register`   | Register a new product.        |

---

### 📝 POST `/products/register`

Registers a new product.

#### 📥 Request Body:

```json
{
  "name": "Smartphone",
  "category": "Electronics",
  "price": 299.99
}
```
#### 📤 Response:
```
{
  "message": "✅ Product registered successfully",
  "product": {
    "id": 1,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 299.99
  }
}
```
## 📦 Inventory

| Method | Endpoint                          | Description                                   |
|--------|-----------------------------------|-----------------------------------------------|
| GET    | `/inventory/`                     | Get all inventory items (paginated).          |
| GET    | `/inventory/low-stock`            | Get items with stock below threshold.         |
| PUT    | `/inventory/update`               | Update stock and log history.                 |
| GET    | `/inventory/{product_id}/history` | Get stock change history for a product.       |

---

### 📋 GET `/inventory/?skip=0&limit=10`

Returns paginated inventory records.

---

### 📉 GET `/inventory/low-stock?threshold=5`

Lists products with stock below a threshold (default threshold is 10).

---

### ✏️ PUT `/inventory/update`

Updates stock for a product and logs the change history.

#### 📥 Request Body:

```json
{
  "product_id": 1,
  "stock": 50
}
```
### 📜 GET /inventory/1/history

Returns historical stock changes for product with ID 


## 📈 Sales

| Method | Endpoint                           | Description                                                        |
|--------|------------------------------------|--------------------------------------------------------------------|
| GET    | `/sales/`                          | Fetch sales, filter by date/category/product.                      |
| GET    | `/sales/revenue`                   | Revenue in specified period (daily, weekly, etc.).                 |
| GET    | `/sales/revenue/compare`           | Compare revenue across two date ranges.                            |
| GET    | `/sales/revenue/by-category`       | Revenue grouped by product category.                               |
| GET    | `/sales/summary`                   | Sales summary by period with quantity & revenue.                   |
| GET    | `/sales/best-sellers`              | Top selling products in a date/category filter.                    |

---

### 📊 GET `/sales/?start_date=2024-01-01&end_date=2024-01-31&category=Electronics`

Returns sales in the given date and category range.

---

### 💰 GET `/sales/revenue?period=monthly`

Returns revenue from the last month.

---

### 🔄 GET `/sales/revenue/compare?start_date_1=2024-01-01&end_date_1=2024-01-31&start_date_2=2024-02-01&end_date_2=2024-02-28`

Compares revenue between two custom date ranges.

---

### 📂 GET `/sales/revenue/by-category`

Returns total revenue grouped by product category.

---

### 📆 GET `/sales/summary?period=weekly&category=Books`

Returns weekly sales summaries for the *Books* category.

---

### 🏆 GET `/sales/best-sellers?top_n=5&category=Books`

Returns the top 5 best-selling products in the *Books* category.

## 🧩 Dependencies

The project uses the following key dependencies:

- **FastAPI** – Web framework for building APIs
- **SQLAlchemy** – ORM for interacting with the PostgreSQL database
- **Uvicorn** – ASGI server for running FastAPI
- **Psycopg2** – PostgreSQL database adapter
- **Pydantic** – Data validation and settings management

📦 **Install all dependencies via:**

```bash
pip install -r requirements.txt
```

### 🧪 Sample Data

You can populate the database with demo products, inventory, and sales data by running the seed script:
```bash
python seed_db.py

python -m app.seed_db --force
```
