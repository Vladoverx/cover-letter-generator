from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Job and company information
    job_title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=False)
    
    # Generated content
    content = Column(Text, nullable=False)
    
    # Metadata
    title = Column(String(255), nullable=True)  # User-defined title for the cover letter
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="cover_letters") 