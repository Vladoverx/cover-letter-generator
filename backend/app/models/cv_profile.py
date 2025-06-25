from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class CVProfile(Base):
    __tablename__ = "cv_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Personal information
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    
    # Professional summary
    summary = Column(Text, nullable=True)
    
    # Structured data using JSON columns for better type safety and querying
    skills = Column(JSON, nullable=True)  # Store as list of skill objects
    experience = Column(JSON, nullable=True)  # Store as list of experience objects
    education = Column(JSON, nullable=True)  # Store as list of education objects
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # One-to-one relationship with user
    user = relationship("User", back_populates="cv_profile") 