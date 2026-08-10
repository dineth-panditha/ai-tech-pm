from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_agent import chat_with_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/ask")
def ask_project_manager(request: ChatRequest):
    ai_response = chat_with_agent(request.message)
    
    return {
        "response": ai_response
    }