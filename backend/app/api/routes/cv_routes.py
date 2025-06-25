from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from ...core.dependencies import (
    SessionDep,
    CVServiceDep,
    validate_cv_profile_exists,
    validate_user_exists
)
from ...schemas import cv_profile as cv_schemas
from ...models.cv_profile import CVProfile

router = APIRouter(
    prefix="/cv",
    tags=["cv"],
    responses={404: {"description": "Not found"}}
)


@router.post("/profile", response_model=cv_schemas.CVProfile)
async def create_cv_profile(
    cv_profile: cv_schemas.CVProfileCreate,
    db: SessionDep,
    cv_service: CVServiceDep
):
    """Create CV profile from manual data entry"""
    return cv_service.create_cv_profile(db=db, cv_profile=cv_profile)


@router.get("/profile/{profile_id}", response_model=cv_schemas.CVProfile)
async def get_cv_profile(
    cv_profile: Annotated[CVProfile, Depends(validate_cv_profile_exists)],
    db: SessionDep,
    cv_service: CVServiceDep
):
    """Get CV profile by profile ID"""
    return cv_profile


@router.get("/profile/user/{user_id}", response_model=cv_schemas.CVProfile)
async def get_cv_profile_by_user(
    user: Annotated[object, Depends(validate_user_exists)],
    db: SessionDep,
    cv_service: CVServiceDep
):
    """Get CV profile by user ID"""
    cv_profile = cv_service.get_cv_profile_by_user(db, user_id=user.id)
    if not cv_profile:
        raise HTTPException(status_code=404, detail="CV profile not found for user")
    return cv_profile


@router.put("/profile/{profile_id}", response_model=cv_schemas.CVProfile)
async def update_cv_profile(
    cv_profile: Annotated[CVProfile, Depends(validate_cv_profile_exists)],
    cv_update: cv_schemas.CVProfileUpdate,
    db: SessionDep,
    cv_service: CVServiceDep
):
    """Update CV profile"""
    return cv_service.update_cv_profile(
        db=db, 
        cv_profile=cv_profile, 
        cv_update=cv_update
    )


@router.delete("/profile/{profile_id}")
async def delete_cv_profile(
    cv_profile: Annotated[CVProfile, Depends(validate_cv_profile_exists)],
    db: SessionDep,
    cv_service: CVServiceDep
):
    """Delete CV profile"""
    success = cv_service.delete_cv_profile(db=db, cv_profile=cv_profile)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete CV profile")
    return {"message": "CV profile deleted successfully"}

