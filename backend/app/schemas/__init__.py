# Import all schemas
from .user import User, UserCreate, UserUpdate
from .cv_profile import (
    CVProfile, 
    CVProfileCreate, 
    CVProfileUpdate, 
    SkillSchema,
    ExperienceSchema,
    EducationSchema
)
from .cover_letter import CoverLetter, CoverLetterCreate, CoverLetterUpdate, CoverLetterGenerate

# Rebuild models to resolve forward references
# This is required for Pydantic v2 when using forward references
User.model_rebuild()

# Make schemas available for import
__all__ = [
    # User schemas
    "User", "UserCreate", "UserUpdate",
    # CV Profile schemas
    "CVProfile", "CVProfileCreate", "CVProfileUpdate",
    "SkillSchema", "ExperienceSchema", "EducationSchema",
    # Cover Letter schemas
    "CoverLetter", "CoverLetterCreate", "CoverLetterUpdate", "CoverLetterGenerate"
] 