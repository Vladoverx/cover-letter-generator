from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import HTTPException

from ...core.dependencies import (
    SessionDep,
    CoverLetterServiceDep,
    UserServiceDep,
    CVServiceDep,
    SettingsDep,
    validate_cover_letter_exists,
    validate_user_exists
)
from ...schemas import cover_letter as cover_letter_schemas
from ...models.cover_letter import CoverLetter
from ...models.user import User

router = APIRouter(
    prefix="/cover-letters",
    tags=["cover-letters"],
    responses={404: {"description": "Not found"}}
)


@router.post("/generate", response_model=cover_letter_schemas.CoverLetterResponse)
async def generate_cover_letter(
    request: cover_letter_schemas.CoverLetterGenerate,
    db: SessionDep,
    cover_letter_service: CoverLetterServiceDep,
    user_service: UserServiceDep,
    cv_service: CVServiceDep,
    settings: SettingsDep
):
    """Generate a new cover letter based on CV profile and job description"""
    user = user_service.get_user(db, user_id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    cv_profile = cv_service.get_cv_profile_by_user(db, user_id=request.user_id)
    if not cv_profile:
        raise HTTPException(status_code=404, detail="CV profile not found for user")
    
    return await cover_letter_service.generate_cover_letter(
        db=db, 
        request=request, 
        settings=settings,
        cv_profile=cv_profile,
        user=user
    )


@router.get("/user/{user_id}", response_model=cover_letter_schemas.CoverLetterListResponse)
async def get_user_cover_letters(
    user: Annotated[User, Depends(validate_user_exists)],
    db: SessionDep,
    cover_letter_service: CoverLetterServiceDep
):
    """Get all cover letters for a user"""
    cover_letters = cover_letter_service.get_cover_letters_by_user(db, user_id=user.id)
    return cover_letters


@router.get("/{cover_letter_id}", response_model=cover_letter_schemas.CoverLetterResponse)
async def get_cover_letter(
    cover_letter: Annotated[CoverLetter, Depends(validate_cover_letter_exists)],
    db: SessionDep,
    cover_letter_service: CoverLetterServiceDep
):
    """Get a specific cover letter by ID"""
    result = cover_letter_service.get_cover_letter(db, cover_letter_id=cover_letter.id)
    if not result:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    return result


@router.put("/{cover_letter_id}", response_model=cover_letter_schemas.CoverLetterResponse)
async def update_cover_letter(
    cover_letter: Annotated[CoverLetter, Depends(validate_cover_letter_exists)],
    cover_letter_update: cover_letter_schemas.CoverLetterUpdate,
    db: SessionDep,
    cover_letter_service: CoverLetterServiceDep
):
    """Update a cover letter"""
    updated_cover_letter = cover_letter_service.update_cover_letter(
        db=db, 
        cover_letter_id=cover_letter.id, 
        cover_letter_update=cover_letter_update
    )
    if not updated_cover_letter:
        raise HTTPException(status_code=500, detail="Failed to update cover letter")
    return updated_cover_letter


@router.delete("/{cover_letter_id}")
async def delete_cover_letter(
    cover_letter: Annotated[CoverLetter, Depends(validate_cover_letter_exists)],
    db: SessionDep,
    cover_letter_service: CoverLetterServiceDep
):
    """Delete a cover letter"""
    success = cover_letter_service.delete_cover_letter(db=db, cover_letter_id=cover_letter.id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete cover letter")
    return {"message": "Cover letter deleted successfully"}


@router.post("/", response_model=cover_letter_schemas.CoverLetterResponse)
async def create_cover_letter(
    cover_letter_data: cover_letter_schemas.CoverLetterCreate,
    db: SessionDep,
    cover_letter_service: CoverLetterServiceDep,
    user_service: UserServiceDep
):
    """Create a new cover letter manually"""
    # Validate user exists
    user = user_service.get_user(db, user_id=cover_letter_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return cover_letter_service.create_cover_letter(db=db, cover_letter=cover_letter_data) 