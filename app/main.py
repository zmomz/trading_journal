from fastapi import FastAPI
from app.database import engine, Base
from app.api.v1.router import api_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Trading Journal API", version="1.0")

# Include API routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Trading Journal API"}
