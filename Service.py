"""
Service.py
----------
Business logic layer. Contains all database operations and domain rules.

This layer is called by Controller.py and has no knowledge of HTTP.
It receives a SQLAlchemy Session via dependency injection.
"""

from sqlalchemy.orm import Session
from models import User, Category, Product, Order, Role


def create_user(db: Session, username: str, email: str, password: str, role_id: int = None) -> User:
    """
    Create and persist a new user.

    Args:
        db: Database session.
        username: Unique username.
        email: User email address.
        password: Plain text password (hash before storing in production).
        role_id: Optional role ID to assign to the user.

    Returns:
        The created User object with its generated ID.
    """
    user = User(username=username, email=email, password=password, Role_id=role_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int = None):
    """
    Retrieve one or all users.

    Args:
        db: Database session.
        user_id: If provided, returns the specific user. If None, returns all users.

    Returns:
        A single User object or a list of all User objects.

    Raises:
        ValueError: If a specific user_id is given but not found.
    """
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ValueError("User not found")
        return user
    return db.query(User).all()


def create_category(db: Session, name: str, description: str) -> Category:
    """
    Create and persist a new product category.

    Args:
        db: Database session.
        name: Category name.
        description: Optional category description.

    Returns:
        The created Category object with its generated ID.
    """
    category = Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def create_product(db: Session, name: str, description: str, price: float, category_id: int, quantity: int,image:str) -> Product:
    """
    Create and persist a new product.

    Args:
        db: Database session.
        name: Product name.
        description: Optional product description.
        price: Product price (must be > 0).
        category_id: Foreign key to an existing Category.
        quantity: Available stock quantity.

    Returns:
        The created Product object with its generated ID.
    """
    product = Product(name=name, description=description, price=price, category_id=category_id, quantity=quantity,image=image)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def create_order(db: Session, user_id: int, product_id: int, quantity: int) -> Order:
    """
    Create a new order and deduct stock from the product.

    Validates that the product exists and has sufficient stock before
    creating the order. Stock is decremented atomically in the same transaction.

    Args:
        db: Database session.
        user_id: ID of the user placing the order.
        product_id: ID of the product being ordered.
        quantity: Number of units to order.

    Returns:
        The created Order object with its generated ID.

    Raises:
        ValueError: If the product is not found or stock is insufficient.
    """
    # Fetch the product first
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise ValueError("Product not found")

    # Check stock
    if quantity > product.quantity:
        raise ValueError("Not enough product in stock")

    # Deduct stock
    product.quantity -= quantity

    # Create the order
    order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int = None):
    """
    Retrieve one or all orders.

    Args:
        db: Database session.
        order_id: If provided, returns the specific order. If None, returns all orders.

    Returns:
        A single Order object or a list of all Order objects.

    Raises:
        ValueError: If a specific order_id is given but not found.
    """
    if order_id:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order is None:
            raise ValueError("Order not found")
        return order
    return db.query(Order).all()


def get_product(db: Session, product_id: int = None):
    """
    Retrieve one or all products.

    Args:
        db: Database session.
        product_id: If provided, returns the specific product. If None, returns all products.

    Returns:
        A single Product object or a list of all Product objects.

    Raises:
        ValueError: If a specific product_id is given but not found.
    """
    if product_id:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise ValueError("Product not found")
        return product
    return db.query(Product).all()

def create_role(db: Session, name: str) -> Role:
    """
    Create and persist a new role.

    Args:
        db: Database session.
        name: Role name.

    Returns:
        The created Role object with its generated ID.
    """
    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_role(db: Session, role_id: int = None):
    """
    Retrieve one or all roles.

    Args:
        db: Database session.
        role_id: If provided, returns the specific role. If None, returns all roles.
    Returns:
        A single Role object or a list of all Role objects.
    Raises:
        ValueError: If a specific role_id is given but not found.
    """
    if role_id:
        role = db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise ValueError("Role not found")
        return role
    return db.query(Role).all()


def get_roles(db: Session):
    """
    Retrieve all roles.

    Args:
        db: Database session.

    Returns:
        A list of all Role objects.
    """
    return get_role(db)  
        
def update_role(db: Session, role_id: int, name: str) -> Role:
    """
    Update an existing role's name.

    Args:
        db: Database session.
        role_id: ID of the role to update.
        name: New name for the role.

    Returns:
        The updated Role object.

    Raises:
        ValueError: If the role with the given ID is not found.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise ValueError("Role not found")
    role.name = name
    db.commit()
    db.refresh(role)
    return role


def get_users_by_role(db: Session, role_id: int):
    """
    Retrieve all users that belong to a specific role.

    Args:
        db: Database session.
        role_id: ID of the role to filter by.

    Returns:
        A list of User objects with the specified role_id.

    Raises:
        ValueError: If no role with the given ID exists.
    """
    # Verify the role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise ValueError("Role not found")
    
    # Get all users with this role
    users = db.query(User).filter(User.Role_id == role_id).all()
    return users