from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import health

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION
    )

    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Production එකේදී මේක ["http://localhost:3000"] වගේ වෙනස් කරනවා
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    application.include_router(health.router, prefix="/api/v1/health", tags=["Health Check"])

    return application

app = get_application()