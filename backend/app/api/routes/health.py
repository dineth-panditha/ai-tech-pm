from fastapi import APIRouter, Depends
from supabase import Client
from app.core.database import get_supabase_client

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "AI Project Manager API is running successfully!"}

@router.get("/db-status")
def check_db(supabase: Client = Depends(get_supabase_client)):
   
    if supabase:
        return {"status": "Connected to Supabase PostgreSQL"}
    return {"status": "Database connection failed"}