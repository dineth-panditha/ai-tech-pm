from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import health, chat

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION
    )

    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    application.include_router(health.router, prefix="/api/v1/health", tags=["Health Check"])
    application.include_router(chat.router, prefix="/api/v1/chat", tags=["AI Chat"])

    return application

app = get_application()