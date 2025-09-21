from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.exceptions import HTTPException
from src.services.access_control_service import AccessControlService
from src.models.user_session import UserSessionModel
import logging

logger = logging.getLogger("access_control_middleware")

class AccessControlMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, access_control_service: AccessControlService):
        super().__init__(app)
        self.access_control_service = access_control_service
    
    async def dispatch(self, request: Request, call_next):
        # Skip access control for certain paths
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)
        
        # Skip access control if no user is authenticated
        if not hasattr(request.state, "user") or request.state.user is None:
            return await call_next(request)
        
        user_session = request.state.user
        
        # Determine resource and action based on request
        resource = None
        action = None
        
        if request.url.path.startswith("/directories/"):
            resource = f"directory:{request.url.path[13:]}"  # Remove "/directories/" prefix
            if request.method == "GET":
                action = "list"
        elif request.url.path.startswith("/files/"):
            resource = f"file:{request.url.path[7:]}"  # Remove "/files/" prefix
            if request.method == "GET":
                action = "read"
        
        # If we can't determine resource or action, proceed without access control
        if not resource or not action:
            return await call_next(request)
        
        # Check access
        if not self.access_control_service.check_access(user_session, resource, action):
            logger.warning(f"Access denied for user {user_session.principal} to {resource} with action {action}")
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Continue with the request
        response = await call_next(request)
        return response