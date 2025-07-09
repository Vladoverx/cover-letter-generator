from typing import List, Optional
from sqlalchemy.orm import Session
from google import genai
from fastapi import HTTPException
import logging

from ..models.cover_letter import CoverLetter
from ..schemas.cover_letter import (
    CoverLetterCreate, 
    CoverLetterUpdate, 
    CoverLetterGenerate,
    CoverLetterResponse,
    CoverLetterListResponse
)
from ..core.config import Settings
from ..services.cv_service import get_cv_profile_by_user
from ..services.user_service import get_user

logger = logging.getLogger(__name__)


async def generate_cover_letter(
    db: Session, 
    request: CoverLetterGenerate, 
    settings: Settings,
    cv_profile,
    user
) -> CoverLetterResponse:
    """Generate a cover letter based on CV profile and job description using LLM"""
    logger.info(f"Generating cover letter for user {request.user_id}")
    
    if not cv_profile:
        logger.error(f"CV profile not found for user {request.user_id}")
        raise HTTPException(status_code=404, detail="CV profile not found for user")
    
    if not user:
        logger.error(f"User not found with ID {request.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        content = await generate_cover_letter_content(cv_profile, request, settings)
        logger.info(f"Successfully generated cover letter content for user {request.user_id}")
        
        cover_letter_data = CoverLetterCreate(
            user_id=request.user_id,
            job_title=request.job_title,
            company_name=request.company_name,
            job_description=request.job_description,
            content=content,
            title=f"Cover Letter for {request.job_title or 'Position'}" + 
                  (f" at {request.company_name}" if request.company_name else "")
        )
        
        return create_cover_letter(db, cover_letter_data)
    except Exception as e:
        logger.error(f"Failed to generate cover letter: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate cover letter: {str(e)}")


async def generate_cover_letter_content(cv_profile, request: CoverLetterGenerate, settings: Settings) -> str:
    """Generate cover letter content using Google Gemini LLM"""
    try:
        cv_summary = _format_cv_for_prompt(cv_profile)
        
        prompt = _build_cover_letter_prompt(cv_summary, request)

        # Ensure the API key is configured before attempting to call Gemini
        if not settings.google_api_key:
            logger.error("Google API key is missing; cannot generate cover letter content")
            raise HTTPException(
                status_code=500,
                detail="Google API key is not configured on the server."
            )

        client = genai.Client(api_key=settings.google_api_key)
        
        # Generate content using the client's models.generate_content method
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Error generating content with Gemini: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate cover letter content: {str(e)}"
        )


def _format_cv_for_prompt(cv_profile) -> str:
    """Format CV profile data for the LLM prompt"""
    cv_parts = []
    
    # Basic info
    if hasattr(cv_profile, 'full_name') and cv_profile.full_name:
        cv_parts.append(f"Name: {cv_profile.full_name}")
    
    if hasattr(cv_profile, 'email') and cv_profile.email:
        cv_parts.append(f"Email: {cv_profile.email}")
    
    if hasattr(cv_profile, 'phone') and cv_profile.phone:
        cv_parts.append(f"Phone: {cv_profile.phone}")
    
    # Professional summary
    if hasattr(cv_profile, 'summary') and cv_profile.summary:
        cv_parts.append(f"Professional Summary: {cv_profile.summary}")
    
    # Skills
    if hasattr(cv_profile, 'skills') and cv_profile.skills:
        skills_text = _format_skills_for_prompt(cv_profile.skills)
        if skills_text:
            cv_parts.append(f"Skills: {skills_text}")
    
    # Experience
    if hasattr(cv_profile, 'experience') and cv_profile.experience:
        experience_text = _format_experience_for_prompt(cv_profile.experience)
        if experience_text:
            cv_parts.append(f"Work Experience: {experience_text}")

    if hasattr(cv_profile, 'projects') and cv_profile.projects:
        projects_text = _format_projects_for_prompt(cv_profile.projects)
        if projects_text:
            cv_parts.append(f"Projects: {projects_text}")
    
    # Education
    if hasattr(cv_profile, 'education') and cv_profile.education:
        education_text = _format_education_for_prompt(cv_profile.education)
        if education_text:
            cv_parts.append(f"Education: {education_text}")
    
    return "\n".join(cv_parts)


def _format_skills_for_prompt(skills_data: List[dict]) -> str:
    """Format skills data for the prompt"""
    if not skills_data:
        return ""
    
    skills_by_category = {}
    for skill in skills_data:
        if isinstance(skill, dict):
            category = skill.get('category', 'General')
            if category not in skills_by_category:
                skills_by_category[category] = []
            
            skill_name = skill.get('name', '')
            proficiency = skill.get('proficiency', '')
            if proficiency:
                skill_name += f" ({proficiency})"
            skills_by_category[category].append(skill_name)
    
    formatted_skills = []
    for category, category_skills in skills_by_category.items():
        if category_skills:
            skills_list = ", ".join(category_skills)
            formatted_skills.append(f"{category}: {skills_list}")
    
    return "; ".join(formatted_skills)


def _format_experience_for_prompt(experience_data: List[dict]) -> str:
    """Format experience data for the prompt"""
    if not experience_data:
        return ""
    
    formatted_experience = []
    for exp in experience_data:
        if isinstance(exp, dict):
            title = exp.get('title', '')
            company = exp.get('company', '')
            start_date = exp.get('start_date', '')
            end_date = exp.get('end_date', 'Present')
            description = exp.get('description', '')
            
            exp_parts = []
            if title:
                exp_parts.append(title)
            if company:
                exp_parts.append(f"at {company}")
            if start_date:
                exp_parts.append(f"({start_date} - {end_date})")
            if description:
                exp_parts.append(f"- {description}")
            
            if exp_parts:
                formatted_experience.append(" ".join(exp_parts))
    
    return "; ".join(formatted_experience)


def _format_projects_for_prompt(projects_data: List[dict]) -> str:
    """Format projects data for the prompt"""
    if not projects_data:
        return ""
    
    formatted_projects = []
    for proj in projects_data:
        if isinstance(proj, dict):
            name = proj.get('name', '')
            description = proj.get('description', '')
            technologies = proj.get('technologies', '')

            proj_parts = []
            if name:
                proj_parts.append(name)
            if description:
                proj_parts.append(f"- {description}")
            if technologies:
                proj_parts.append(f"Technologies: {technologies}")

            if proj_parts:
                formatted_projects.append(" ".join(proj_parts))
    
    return "; ".join(formatted_projects)


def _format_education_for_prompt(education_data: List[dict]) -> str:
    """Format education data for the prompt"""
    if not education_data:
        return ""
    
    formatted_education = []
    for edu in education_data:
        if isinstance(edu, dict):
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            end_date = edu.get('end_date', '')
            grade = edu.get('grade', '')
            
            edu_parts = []
            if degree:
                edu_parts.append(degree)
            if institution:
                edu_parts.append(f"from {institution}")
            if end_date:
                edu_parts.append(f"({end_date})")
            if grade:
                edu_parts.append(f"Grade: {grade}")
            
            if edu_parts:
                formatted_education.append(" ".join(edu_parts))
    
    return "; ".join(formatted_education)


def _build_cover_letter_prompt(cv_summary: str, request: CoverLetterGenerate) -> str:
    """Build the prompt for the LLM to generate the cover letter"""
    company_part = f" at {request.company_name}" if request.company_name else ""
    position_part = request.job_title or "the position"
    
    prompt = f"""Generate a professional cover letter based on the following CV and job description. 
The cover letter must be less than 120 words and should be personalized, engaging, and highlight the most relevant qualifications.

CV INFORMATION:
{cv_summary}

JOB DETAILS:
Position: {position_part}{company_part}
Job Description: {request.job_description}

REQUIREMENTS:
- Maximum 120 words
- Professional tone
- Highlight most relevant skills and experience from the CV
- Address the specific job requirements mentioned in the job description
- Include a proper greeting and closing
- Be concise but impactful
- Focus on value proposition for the employer

Generate the cover letter now:"""
    
    return prompt


def get_cover_letter(db: Session, cover_letter_id: int) -> Optional[CoverLetterResponse]:
    """Get cover letter by ID"""
    db_cover_letter = db.query(CoverLetter).filter(CoverLetter.id == cover_letter_id).first()
    if db_cover_letter:
        return CoverLetterResponse.model_validate(db_cover_letter)
    return None


def get_cover_letters_by_user(db: Session, user_id: int) -> CoverLetterListResponse:
    """Get cover letters by user ID with default limit"""
    cover_letters = (
        db.query(CoverLetter)
        .filter(CoverLetter.user_id == user_id)
        .order_by(CoverLetter.created_at.desc())
        .limit(50)
        .all()
    )
    return CoverLetterListResponse(
        total=len(cover_letters),
        items=[CoverLetterResponse.model_validate(cl) for cl in cover_letters]
    )


def create_cover_letter(db: Session, cover_letter: CoverLetterCreate) -> CoverLetterResponse:
    """Create a new cover letter"""
    db_cover_letter = CoverLetter(**cover_letter.model_dump())
    db.add(db_cover_letter)
    db.commit()
    db.refresh(db_cover_letter)
    return CoverLetterResponse.model_validate(db_cover_letter)


def update_cover_letter(
    db: Session, 
    cover_letter_id: int, 
    cover_letter_update: CoverLetterUpdate
) -> Optional[CoverLetterResponse]:
    """Update an existing cover letter"""
    db_cover_letter = db.query(CoverLetter).filter(CoverLetter.id == cover_letter_id).first()
    if db_cover_letter:
        update_data = cover_letter_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cover_letter, field, value)
        db.commit()
        db.refresh(db_cover_letter)
        return CoverLetterResponse.model_validate(db_cover_letter)
    return None


def delete_cover_letter(db: Session, cover_letter_id: int) -> bool:
    """Delete a cover letter"""
    db_cover_letter = db.query(CoverLetter).filter(CoverLetter.id == cover_letter_id).first()
    if db_cover_letter:
        db.delete(db_cover_letter)
        db.commit()
        return True
    return False