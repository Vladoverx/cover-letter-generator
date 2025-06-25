from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from ...core.dependencies import (
    SessionDep,
    UserServiceDep,
    validate_user_exists
)
from ...schemas import user as user_schemas
from ...models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}}
)


@router.post("/", response_model=user_schemas.User)
async def create_user(
    user: user_schemas.UserCreate,
    db: SessionDep,
    user_service: UserServiceDep
):
    """Create a new user"""
    # Check if user already exists (this will be handled by the service)
    try:
        return user_service.create_user(db=db, user=user)
    except HTTPException:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.get("/{user_id}", response_model=user_schemas.User)
async def get_user(
    user: Annotated[User, Depends(validate_user_exists)]
):
    """Get user by ID"""
    return user


@router.put("/{user_id}", response_model=user_schemas.User)
async def update_user(
    user: Annotated[User, Depends(validate_user_exists)],
    user_update: user_schemas.UserUpdate,
    db: SessionDep,
    user_service: UserServiceDep
):
    """Update user information"""
    try:
        updated_user = user_service.update_user(
            db=db, 
            user_id=user.id, 
            user_update=user_update
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except HTTPException:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.delete("/{user_id}")
async def delete_user(
    user: Annotated[User, Depends(validate_user_exists)],
    db: SessionDep,
    user_service: UserServiceDep
):
    """Delete user and all related data"""
    try:
        success = user_service.delete_user(db=db, user_id=user.id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete user")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete user")


@router.get("/", response_model=list[user_schemas.User])
async def list_users(
    db: SessionDep,
    user_service: UserServiceDep
):
    """List all users (for development/admin purposes)"""
    users = user_service.get_users(db)
    return users