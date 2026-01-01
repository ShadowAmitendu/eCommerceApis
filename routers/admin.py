from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.product import Product
from schemas.user import UserOut
from schemas.product import ProductOut
from dependencies.roles import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=List[UserOut])
def get_all_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        user=Depends(require_role("admin")),
        db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(
        user_id: int,
        user=Depends(require_role("admin")),
        db: Session = Depends(get_db)
):
    """Get a specific user by ID (admin only)"""
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return target_user


@router.put("/users/{user_id}/deactivate")
def deactivate_user(
        user_id: int,
        user=Depends(require_role("admin")),
        db: Session = Depends(get_db)
):
    """Deactivate a user account (admin only)"""
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if target_user.id == user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )

    target_user.is_active = 0
    db.commit()

    return {"message": f"User {target_user.email} has been deactivated"}


@router.put("/users/{user_id}/activate")
def activate_user(
        user_id: int,
        user=Depends(require_role("admin")),
        db: Session = Depends(get_db)
):
    """Activate a user account (admin only)"""
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    target_user.is_active = 1
    db.commit()

    return {"message": f"User {target_user.email} has been activated"}


@router.get("/products/all", response_model=List[ProductOut])
def get_all_products(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        include_inactive: bool = False,
        user=Depends(require_role("admin")),
        db: Session = Depends(get_db)
):
    """Get all products including inactive ones (admin only)"""
    query = db.query(Product)

    if not include_inactive:
        query = query.filter(Product.is_active == 1)

    products = query.offset(skip).limit(limit).all()
    return products


@router.delete("/products/{product_id}")
def hard_delete_product(
        product_id: int,
        user=Depends(require_role("admin")),
        db: Session = Depends(get_db)
):
    """Permanently delete a product (admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {"message": f"Product {product.name} has been permanently deleted"}