from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
import re


# ─── User ────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 50:
            raise ValueError("Username must be at most 50 characters")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


# ─── Category ────────────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        if len(v) < 2:
            raise ValueError("Category name must be at least 2 characters")
        if len(v) > 50:
            raise ValueError("Category name must be at most 50 characters")
        return v.strip()


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {"from_attributes": True}


# ─── Product ─────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category_id: int
    image: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        if len(v) < 2:
            raise ValueError("Product name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Product name must be at most 100 characters")
        return v.strip()

    @field_validator("price")
    @classmethod
    def price_valid(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return round(v, 2)

    @field_validator("quantity")
    @classmethod
    def quantity_valid(cls, v):
        if v < 0:
            raise ValueError("Quantity cannot be negative")
        return v


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    quantity: int
    category_id: int
    image: Optional[str]

    model_config = {"from_attributes": True}


# ─── Order ───────────────────────────────────────────────────────────────────

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_valid(cls, v):
        if v <= 0:
            raise ValueError("Order quantity must be at least 1")
        return v


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = {"from_attributes": True}
