from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from dependencies.auth import get_current_user
from dependencies.roles import require_role
from models.product import Product
from schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductOut])
def get_products(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        search: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """Get all active products with pagination and search"""
    query = db.query(Product).filter(Product.is_active == 1)

    if search:
        query = query.filter(Product.name.contains(search))

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == 1
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
        data: ProductCreate,
        user=Depends(require_role("seller", "admin")),
        db: Session = Depends(get_db)
):
    """Create a new product (sellers and admins only)"""
    # Validate price and stock
    if data.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0"
        )

    if data.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cannot be negative"
        )

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        seller_id=user["user_id"]
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
        product_id: int,
        data: ProductUpdate,
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Update a product (only by owner or admin)"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Check ownership or admin role
    if product.seller_id != user["user_id"] and user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this product"
        )

    # Update fields
    update_data = data.dict(exclude_unset=True)

    # Validate values if provided
    if "price" in update_data and update_data["price"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0"
        )

    if "stock" in update_data and update_data["stock"] < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cannot be negative"
        )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
        product_id: int,
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Delete a product (soft delete - only by owner or admin)"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Check ownership or admin role
    if product.seller_id != user["user_id"] and user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this product"
        )

    # Soft delete
    product.is_active = 0
    db.commit()

    return None
