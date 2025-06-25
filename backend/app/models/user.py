from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # One-to-one relationship with CV profile
    cv_profile = relationship(
        "CVProfile", 
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False
    )
    cover_letters = relationship(
        "CoverLetter", 
        back_populates="user",
        cascade="all, delete-orphan"
    ) 