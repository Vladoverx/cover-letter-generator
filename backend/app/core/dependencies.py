from typing import Annotated
from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm import Session

from .database import get_db
from .config import get_settings, Settings
from ..services import cv_service, user_service, cover_letter_service
from ..models.user import User
from ..models.cv_profile import CVProfile
from ..models.cover_letter import CoverLetter


# Database session dependency
SessionDep = Annotated[Session, Depends(get_db)]

# Settings dependency
SettingsDep = Annotated[Settings, Depends(get_settings)]


# Service dependencies
def get_cv_service():
    """Dependency to get CV service module"""
    return cv_service


def get_user_service():
    """Dependency to get user service module"""
    return user_service


def get_cover_letter_service():
    """Dependency to get cover letter service module"""
    return cover_letter_service


# Type annotations for service dependencies
CVServiceDep = Annotated[type(cv_service), Depends(get_cv_service)]
UserServiceDep = Annotated[type(user_service), Depends(get_user_service)]
CoverLetterServiceDep = Annotated[type(cover_letter_service), Depends(get_cover_letter_service)]


# Validation dependencies
async def validate_user_exists(
    user_id: Annotated[int, Path()], 
    db: SessionDep, 
    user_svc: UserServiceDep
) -> User:
    """Dependency to validate user exists and return user object"""
    user = user_svc.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def validate_cv_profile_exists(
    profile_id: Annotated[int, Path()], 
    db: SessionDep, 
    cv_svc: CVServiceDep
) -> CVProfile:
    """Dependency to validate CV profile exists and return profile object"""
    cv_profile = cv_svc.get_cv_profile(db, profile_id=profile_id)
    if not cv_profile:
        raise HTTPException(status_code=404, detail="CV profile not found")
    return cv_profile


async def validate_cover_letter_exists(
    cover_letter_id: Annotated[int, Path()], 
    db: SessionDep, 
    cl_svc: CoverLetterServiceDep
) -> CoverLetter:
    """Dependency to validate cover letter exists and return cover letter object"""
    cover_letter = cl_svc.get_cover_letter(db, cover_letter_id=cover_letter_id)
    if not cover_letter:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    return cover_letter


async def validate_user_has_cv_profile(
    user_id: Annotated[int, Path()], 
    db: SessionDep, 
    cv_svc: CVServiceDep
) -> CVProfile:
    """Dependency to validate user has a CV profile and return it"""
    cv_profile = cv_svc.get_cv_profile_by_user(db, user_id=user_id)
    if not cv_profile:
        raise HTTPException(status_code=404, detail="CV profile not found for user")
    return cv_profile


# For request body validation (when user_id comes from request, not path)
async def validate_user_has_cv_profile_from_request(
    request_user_id: int,
    db: SessionDep, 
    cv_svc: CVServiceDep
) -> CVProfile:
    """Dependency to validate user has a CV profile using user_id from request body"""
    cv_profile = cv_svc.get_cv_profile_by_user(db, user_id=request_user_id)
    if not cv_profile:
        raise HTTPException(status_code=404, detail="CV profile not found for user")
    return cv_profile
    