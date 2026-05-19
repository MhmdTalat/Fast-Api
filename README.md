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

#### Create User
- **POST** `/users/`
- **Description:** Register a new user with username, email, and password
- **Request Body:**
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "role_id": 1
  }
  ```
- **Response:** `UserOut` object

#### Get All Users
- **GET** `/users/`
- **Description:** Retrieve a list of all users
- **Response:** Array of `UserOut` objects

#### Get User by ID
- **GET** `/users/{user_id}`
- **Description:** Retrieve a specific user by their ID
- **Parameters:** `user_id` (integer)
- **Response:** `UserOut` object

#### Get Users by Role
- **GET** `/users/role/{role_id}`
- **Description:** Retrieve all users that belong to a specific role
- **Parameters:** `role_id` (integer)
- **Response:** Array of `UserOut` objects

---

### Categories

#### Create Category
- **POST** `/category/`
- **Description:** Create a new product category
- **Request Body:**
  ```json
  {
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  }
  ```
- **Response:** `CategoryOut` object

---

### Products

#### Create Product
- **POST** `/product/`
- **Description:** Add a new product to a category with price and stock quantity
- **Request Body:**
  ```json
  {
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "quantity": 10,
    "category_id": 1,
    "image": "laptop.jpg"
  }
  ```
- **Response:** `ProductOut` object

#### Get All Products
- **GET** `/products/`
- **Description:** Retrieve a list of all available products
- **Response:** Array of `ProductOut` objects

#### Get Product by ID
- **GET** `/product/{product_id}`
- **Description:** Retrieve a specific product by its ID
- **Parameters:** `product_id` (integer)
- **Response:** `ProductOut` object

---

### Orders

#### Create Order
- **POST** `/order/`
- **Description:** Place an order for a product. Automatically deducts stock. Returns 500 if product not found or stock is insufficient
- **Request Body:**
  ```json
  {
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
  }
  ```
- **Response:** `OrderOut` object

#### Get All Orders
- **GET** `/orders/`
- **Description:** Retrieve a list of all orders
- **Response:** Array of `OrderOut` objects

#### Get Order by ID
- **GET** `/order/{order_id}`
- **Description:** Retrieve a specific order by its ID
- **Parameters:** `order_id` (integer)
- **Response:** `OrderOut` object

---

### Roles

#### Create Role
- **POST** `/role/`
- **Description:** Create a new user role
- **Request Body:**
  ```json
  {
    "name": "Admin"
  }
  ```
- **Response:** `Role` object

#### Get All Roles
- **GET** `/roles/`
- **Description:** Retrieve a list of all user roles
- **Response:** Array of `Role` objects

#### Get Role by ID
- **GET** `/role/{role_id}`
- **Description:** Retrieve a specific role by its ID
- **Parameters:** `role_id` (integer)
- **Response:** `Role` object

---

## Data Models

### UserCreate
```json
{
  "username": "string (3-50 chars, alphanumeric + underscore)",
  "email": "string (valid email format)",
  "password": "string (min 6 chars)",
  "role_id": "integer (optional)"
}
```

### UserOut
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "Role_id": "integer or null"
}
```

### CategoryCreate
```json
{
  "name": "string (2-50 chars)",
  "description": "string or null"
}
```

### CategoryOut
```json
{
  "id": "integer",
  "name": "string",
  "description": "string or null"
}
```

### ProductCreate
```json
{
  "name": "string (2-100 chars)",
  "description": "string or null",
  "price": "number (must be > 0)",
  "quantity": "integer (must be >= 0)",
  "category_id": "integer",
  "image": "string or null"
}
```

### ProductOut
```json
{
  "id": "integer",
  "name": "string",
  "description": "string or null",
  "price": "number",
  "quantity": "integer",
  "category_id": "integer",
  "image": "string or null"
}
```

### OrderCreate
```json
{
  "user_id": "integer",
  "product_id": "integer",
  "quantity": "integer (must be > 0)"
}
```

### OrderOut
```json
{
  "id": "integer",
  "user_id": "integer",
  "product_id": "integer",
  "quantity": "integer"
}
```

### RoleCreate
```json
{
  "name": "string (2-50 chars)"
}
```

### Role
```json
{
  "id": "integer",
  "name": "string"
}
```

---

## Validation Rules

### User
- Username: 3-50 characters, alphanumeric + underscore only
- Password: Minimum 6 characters
- Email: Valid email format (requires email-validator)

### Category
- Name: 2-50 characters

### Product
- Name: 2-100 characters
- Price: Must be greater than 0 (rounded to 2 decimals)
- Quantity: Cannot be negative

### Order
- Quantity: Must be at least 1
- Stock is automatically deducted when order is placed

### Role
- Name: 2-50 characters

---

## Error Responses

All endpoints return appropriate HTTP status codes:
- **200:** Success
- **422:** Validation Error (invalid request body)
- **404:** Resource not found (when getting by ID)
- **500:** Server error (e.g., insufficient stock for order)

---

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
