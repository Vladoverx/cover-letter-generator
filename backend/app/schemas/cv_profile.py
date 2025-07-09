from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class SkillSchema(BaseModel):
    """Schema for individual skill items"""
    name: str
    proficiency: Optional[str] = None  # e.g., "Beginner", "Intermediate", "Advanced"
    category: Optional[str] = None  # e.g., "Programming", "Language", "Soft Skills"


class ExperienceSchema(BaseModel):
    """Schema for individual experience items"""
    title: str
    company: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None


class EducationSchema(BaseModel):
    """Schema for individual education items"""
    degree: str
    institution: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    grade: Optional[str] = None
    location: Optional[str] = None

class ProjectSchema(BaseModel):
    """Schema for personal/side project items"""
    name: str
    description: Optional[str] = None
    technologies: Optional[List[str]] = None


class CVProfileBase(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None
    summary: Optional[str] = None
    skills: Optional[List[SkillSchema]] = None
    experience: Optional[List[ExperienceSchema]] = None
    projects: Optional[List[ProjectSchema]] = None
    education: Optional[List[EducationSchema]] = None


class CVProfileCreate(CVProfileBase):
    user_id: int


class CVProfileUpdate(CVProfileBase):
    pass


class CVProfile(CVProfileBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None 