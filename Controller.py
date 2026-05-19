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
from schemas import UserCreate, UserOut, CategoryCreate, CategoryOut, ProductCreate, ProductOut, OrderCreate, OrderOut, RoleCreate, Role
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
    return Service.create_user(db, username=data.username, email=data.email, password=data.password, role_id=data.role_id)


@router.get("/users/", response_model=List[UserOut], summary="Get all users")
def read_all_users(db: Session = Depends(get_db)):
    """Retrieve a list of all users."""
    return Service.get_user(db)


@router.get("/users/{user_id}", response_model=UserOut, summary="Get user by ID")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific user by their ID."""
    return Service.get_user(db, user_id=user_id)


@router.post("/category/", response_model=CategoryOut, summary="Create a new category")
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new product category."""
    return Service.create_category(db, name=data.name, description=data.description)


@router.post("/product/", response_model=ProductOut, summary="Create a new product")
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to a category with price and stock quantity."""
    return Service.create_product(db, name=data.name, description=data.description,
                                  price=data.price, category_id=data.category_id, quantity=data.quantity,image=data.image)


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


@router.post("/role/", response_model=Role, summary="Create a new role")
def create_role(data: RoleCreate, db: Session = Depends(get_db)):
    """Create a new user role."""
    return Service.create_role(db, name=data.name)

@router.get("/roles/", response_model=List[Role], summary="Get all roles")
def read_roles(db: Session = Depends(get_db)):
    """Retrieve a list of all user roles."""
    return Service.get_roles(db)

@router.get("/role/{role_id}", response_model=Role, summary="Get role by ID")
def read_role(role_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific role by its ID."""
    return Service.get_role(db, role_id=role_id)

@router.get("/users/role/{role_id}", response_model=List[UserOut], summary="Get users by role ID")
def read_users_by_role(role_id: int, db: Session = Depends(get_db)):
    """Retrieve a list of users that belong to a specific role."""
    return Service.get_users_by_role(db, role_id=role_id)
