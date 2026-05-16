"""
Controller.py
-------------
HTTP routing layer. Defines all API endpoints and delegates business logic to Service.py.

Uses FastAPI's APIRouter so routes can be registered in main.py via include_router().
Database sessions are injected per-request using FastAPI's Depends() mechanism.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import UserCreate, UserOut, CategoryCreate, CategoryOut, ProductCreate, ProductOut, OrderCreate, OrderOut
from typing import List
import Service

router = APIRouter()


def get_db():
    """
    Dependency that provides a database session per request.
    Ensures the session is always closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=UserOut, summary="Create a new user")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with username, email, and password."""
    return Service.create_user(db, username=data.username, email=data.email, password=data.password)


@router.post("/category/", response_model=CategoryOut, summary="Create a new category")
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new product category."""
    return Service.create_category(db, name=data.name, description=data.description)


@router.post("/product/", response_model=ProductOut, summary="Create a new product")
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to a category with price and stock quantity."""
    return Service.create_product(db, name=data.name, description=data.description,
                                  price=data.price, category_id=data.category_id, quantity=data.quantity)


@router.post("/order/", response_model=OrderOut, summary="Place a new order")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    """
    Place an order for a product. Automatically deducts stock.
    Returns 500 if product not found or stock is insufficient.
    """
    return Service.create_order(db, user_id=data.user_id, product_id=data.product_id, quantity=data.quantity)


@router.get("/order/{order_id}", response_model=OrderOut, summary="Get order by ID")
def read_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific order by its ID."""
    return Service.get_order(db, order_id=order_id)


@router.get("/orders/", response_model=List[OrderOut], summary="Get all orders")
def read_all_orders(db: Session = Depends(get_db)):
    """Retrieve a list of all orders."""
    return Service.get_order(db)


@router.get("/products/", response_model=List[ProductOut], summary="Get all products")
def read_products(db: Session = Depends(get_db)):
    """Retrieve a list of all available products."""
    return Service.get_product(db)


@router.get("/product/{product_id}", response_model=ProductOut, summary="Get product by ID")
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific product by its ID."""
    return Service.get_product(db, product_id=product_id)
