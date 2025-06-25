import os
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from .database import Base, engine
from .config import get_settings


def init_db() -> None:
    """Initialize the database by creating all tables"""
    try:
        settings = get_settings()
        print("Creating database tables...")
        
        # Create all tables defined in the models
        Base.metadata.create_all(bind=engine)
        
        print("✓ Database tables created successfully!")
        print(f"✓ Database location: {settings.database_url}")
        
        # Check if database file was created (for SQLite)
        if "sqlite" in settings.database_url:
            db_file = settings.database_url.replace("sqlite:///", "")
            if os.path.exists(db_file):
                print(f"✓ Database file created at: {os.path.abspath(db_file)}")
            else:
                print("⚠ Database file not found, but tables should be created when first accessed")
                
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise


def reset_db() -> None:
    """Reset the database by dropping and recreating all tables"""
    try:
        print("⚠ Resetting database - this will delete all data!")
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("✓ All tables dropped")
        
        # Recreate all tables
        Base.metadata.create_all(bind=engine)
        print("✓ All tables recreated")
        
    except Exception as e:
        print(f"✗ Error resetting database: {e}")
        raise


def check_db_connection() -> bool:
    """Check if database connection is working"""
    try:
        # Create a test session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with SessionLocal() as session:
            # Try to execute a simple query
            session.execute(text("SELECT 1"))
            print("✓ Database connection test successful")
            return True
    except Exception as e:
        print(f"✗ Database connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Allow running this file directly for database initialization
    print("Initializing database...")
    init_db()
    check_db_connection() 