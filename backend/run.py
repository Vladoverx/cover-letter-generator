import uvicorn
from app.core.init_db import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    
    print("Starting FastAPI application...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 