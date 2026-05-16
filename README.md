# FastAPI E-Commerce API

A RESTful API built with FastAPI and SQLAlchemy for managing users, categories, products, and orders.

---

## Project Structure

```
Fast-Api/
├── main.py          # App entry point, registers router
├── Controller.py    # Route definitions (HTTP layer)
├── Service.py       # Business logic layer
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic validation schemas
├── database.py      # Database connection and session
└── requirements.txt # Project dependencies
```

---

## Setup

### 1. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

### 4. Open API docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## API Endpoints

### Users

| Method | Endpoint   | Description     |
|--------|------------|-----------------|
| POST   | /users/    | Create new user |

**Request body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secret123"
}
```

---

### Categories

| Method | Endpoint    | Description         |
|--------|-------------|---------------------|
| POST   | /category/  | Create new category |

**Request body:**
```json
{
  "name": "Electronics",
  "description": "Electronic devices"
}
```

---

### Products

| Method | Endpoint              | Description            |
|--------|-----------------------|------------------------|
| POST   | /product/             | Create new product     |
| GET    | /products/            | Get all products       |
| GET    | /product/{product_id} | Get product by ID      |

**Request body (POST):**
```json
{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 999.99,
  "quantity": 50,
  "category_id": 1,
  "image": "laptop.jpg"
}
```

---

### Orders

| Method | Endpoint            | Description       |
|--------|---------------------|-------------------|
| POST   | /order/             | Create new order  |
| GET    | /orders/            | Get all orders    |
| GET    | /order/{order_id}   | Get order by ID   |

**Request body (POST):**
```json
{
  "user_id": 1,
  "product_id": 1,
  "quantity": 2
}
```

---

## Validation Rules

| Field            | Rule                                          |
|------------------|-----------------------------------------------|
| username         | 3–50 chars, letters/numbers/underscores only  |
| email            | Valid email format                            |
| password         | Minimum 6 characters                         |
| category name    | 2–50 characters                              |
| product name     | 2–100 characters                             |
| product price    | Must be greater than 0                       |
| product quantity | Cannot be negative                           |
| order quantity   | Must be at least 1                           |

---

## Database

Uses SQLite (`test.db`) by default. The database file is created automatically on first run.

To switch to PostgreSQL or MySQL, update `DATABASE_URL` in `database.py`:

```python
# PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost/dbname"

# MySQL
DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
```

---

## Dependencies

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **Pydantic** — data validation
- **Uvicorn** — ASGI server
- **email-validator** — email validation for Pydantic
