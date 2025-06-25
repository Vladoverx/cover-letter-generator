from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 50) -> List[User]:
    """Get list of users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user with validation"""
    # Check if user with this email already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    try:
        db_user = User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to create user due to data integrity constraints"
        )


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user information"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check email uniqueness if being updated
    if "email" in update_data:
        existing_user = get_user_by_email(db, update_data["email"])
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
    
    try:
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to update user due to data integrity constraints"
        )


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user and all related data (cascade)"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    try:
        # Cascade relationships handle deletion of CV profile and cover letters
        db.delete(db_user)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )


def search_users_by_name(db: Session, name_query: str, skip: int = 0, limit: int = 100) -> List[User]:
    """Search users by name (case-insensitive partial match)"""
    return (
        db.query(User)
        .filter(User.name.ilike(f"%{name_query}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def verify_user_exists(db: Session, user_id: int) -> bool:
    """Verify if a user exists"""
    return db.query(User).filter(User.id == user_id).first() is not None


 