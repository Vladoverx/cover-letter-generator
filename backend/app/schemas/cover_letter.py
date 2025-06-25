from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, constr


class CoverLetterBase(BaseModel):
    title: constr(min_length=3, max_length=200) = Field(..., description="Title of the cover letter")
    job_title: constr(min_length=2, max_length=100) = Field(..., description="Title of the job being applied for")
    company_name: Optional[constr(max_length=100)] = Field(None, description="Name of the company")
    job_description: constr(min_length=50, max_length=5000) = Field(..., description="Description of the job")
    content: Optional[constr(max_length=1500)] = Field(None, description="Generated cover letter content")


class CoverLetterCreate(CoverLetterBase):
    user_id: int = Field(..., description="ID of the user this cover letter belongs to")


class CoverLetterUpdate(BaseModel):
    title: Optional[constr(min_length=3, max_length=200)] = None
    content: Optional[constr(max_length=1500)] = None


class CoverLetter(CoverLetterBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class CoverLetterGenerate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "job_title": "Senior Software Engineer",
                "company_name": "Tech Corp",
                "job_description": "We are looking for a senior software engineer with 5+ years of experience in Python and web development..."
            }
        }
    )

    user_id: int = Field(..., description="ID of the user requesting the cover letter")
    job_title: constr(min_length=2, max_length=100) = Field(..., description="Title of the job being applied for")
    company_name: Optional[constr(max_length=100)] = Field(None, description="Name of the company")
    job_description: constr(min_length=50, max_length=5000) = Field(
        ..., 
        description="Description of the job position to generate the cover letter for"
    )


class CoverLetterResponse(CoverLetterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class CoverLetterListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 1,
                "items": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "title": "Cover Letter for Senior Software Engineer at Tech Corp",
                        "job_title": "Senior Software Engineer",
                        "company_name": "Tech Corp",
                        "job_description": "We are looking for a senior software engineer...",
                        "content": "Dear Hiring Manager...",
                        "created_at": "2024-03-20T10:00:00Z",
                        "updated_at": "2024-03-20T10:00:00Z"
                    }
                ]
            }
        }
    )

    total: int
    items: List[CoverLetterResponse] 