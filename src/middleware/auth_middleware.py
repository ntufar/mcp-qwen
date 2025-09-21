from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.exceptions import HTTPException
from src.services.auth_service import AuthService
from src.models.user_session import UserSessionModel
import logging

logger = logging.getLogger("auth_middleware")

class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_service: AuthService):
        super().__init__(app)
        self.auth_service = auth_service
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for certain paths (e.g., health checks)
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)
        
        # Extract authorization header
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            # For some endpoints, we might allow unauthenticated access
            # But for file/directory operations, authentication is required
            if request.url.path.startswith("/directories/") or request.url.path.startswith("/files/"):
                logger.warning(f"Authentication required for {request.url.path}")
                raise HTTPException(status_code=401, detail="Authentication required")
            else:
                # For other endpoints, proceed without authentication
                request.state.user = None
                return await call_next(request)
        
        # Extract token from "Bearer <token>" format
        if not authorization.startswith("Bearer "):
            logger.warning("Invalid authentication scheme")
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        token = authorization[7:]  # Remove "Bearer " prefix
        user_session = self.auth_service.validate_session(token)
        
        if not user_session:
            logger.warning("Invalid or expired token")
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Attach user session to request state
        request.state.user = user_session
        
        # Continue with the request
        response = await call_next(request)
        return response