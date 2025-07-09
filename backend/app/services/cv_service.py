from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.cv_profile import CVProfile
from ..schemas.cv_profile import CVProfileCreate, CVProfileUpdate


def get_cv_profile(db: Session, profile_id: int) -> Optional[CVProfile]:
    """Get CV profile by ID"""
    return db.query(CVProfile).filter(CVProfile.id == profile_id).first()


def get_cv_profile_by_user(db: Session, user_id: int) -> Optional[CVProfile]:
    """Get CV profile by user ID (one-to-one relationship)"""
    return db.query(CVProfile).filter(CVProfile.user_id == user_id).first()


def create_cv_profile(db: Session, cv_profile: CVProfileCreate) -> CVProfile:
    """Create a new CV profile (one per user)"""
    # Check if user already has a CV profile
    if get_cv_profile_by_user(db, cv_profile.user_id):
        raise HTTPException(
            status_code=400,
            detail="User already has a CV profile. Use update instead."
        )
    
    # Convert Pydantic models to dictionaries for JSON storage
    cv_profile_dict = cv_profile.model_dump()
    
    # Handle nested objects for JSON storage
    if cv_profile.skills:
        cv_profile_dict['skills'] = [skill.model_dump() for skill in cv_profile.skills]
    
    if cv_profile.experience:
        cv_profile_dict['experience'] = [exp.model_dump() for exp in cv_profile.experience]
    
    if cv_profile.education:
        cv_profile_dict['education'] = [edu.model_dump() for edu in cv_profile.education]

    if cv_profile.projects:
        cv_profile_dict['projects'] = [proj.model_dump() for proj in cv_profile.projects]
    
    db_cv_profile = CVProfile(**cv_profile_dict)
    db.add(db_cv_profile)
    db.commit()
    db.refresh(db_cv_profile)
    return db_cv_profile


def update_cv_profile(db: Session, cv_profile: CVProfile, cv_update: CVProfileUpdate) -> CVProfile:
    """Update CV profile"""
    update_data = cv_update.model_dump(exclude_unset=True)
    
    # Handle nested objects for JSON storage
    for field in ['skills', 'experience', 'education', 'projects']:
        if field in update_data and update_data[field] is not None:
            update_data[field] = [
                item.model_dump() if hasattr(item, 'model_dump') else item 
                for item in update_data[field]
            ]
    
    for key, value in update_data.items():
        setattr(cv_profile, key, value)
    
    db.commit()
    db.refresh(cv_profile)
    return cv_profile


def delete_cv_profile(db: Session, cv_profile: CVProfile) -> bool:
    """Delete CV profile"""
    db.delete(cv_profile)
    db.commit()
    return True