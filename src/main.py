from fastapi import FastAPI
from src.api.directories import router as directories_router
from src.api.files import router as files_router
from src.services.auth_service import AuthService
from src.services.access_control_service import AccessControlService
from src.services.audit_service import AuditService
from src.middleware.auth_middleware import AuthenticationMiddleware
from src.middleware.access_control_middleware import AccessControlMiddleware
from src.middleware.audit_logging_middleware import AuditLoggingMiddleware

app = FastAPI(title="MCP Server for LLM File Browsing")

# Initialize services
auth_service = AuthService()
access_control_service = AccessControlService()
audit_service = AuditService()

# Add middleware
app.add_middleware(AuthenticationMiddleware, auth_service=auth_service)
app.add_middleware(AccessControlMiddleware, access_control_service=access_control_service)
app.add_middleware(AuditLoggingMiddleware, audit_service=audit_service)

# Include routers
app.include_router(directories_router)
app.include_router(files_router)

if __name__ == "__main__":
    import uvicorn
    from src.config import settings
    
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )