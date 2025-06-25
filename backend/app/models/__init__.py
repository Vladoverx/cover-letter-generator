# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .cv_profile import CVProfile
from .cover_letter import CoverLetter

# Make models available for import
__all__ = ["User", "CVProfile", "CoverLetter"] 