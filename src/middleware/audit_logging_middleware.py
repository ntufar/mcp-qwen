from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging
import time
from src.services.audit_service import AuditService
from src.models.user_session import UserSessionModel

logger = logging.getLogger("audit_middleware")

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, audit_service: AuditService):
        super().__init__(app)
        self.audit_service = audit_service
    
    async def dispatch(self, request: Request, call_next):
        # Record start time
        start_time = time.time()
        
        # Get user information if available
        user_principal = "anonymous"
        if hasattr(request.state, "user") and request.state.user:
            user_principal = request.state.user.principal
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Log the request
        logger.info(f"Request: {request.method} {request.url.path} from {user_principal} ({client_ip})")
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log the response
            logger.info(f"Response: {response.status_code} for {request.method} {request.url.path} (Duration: {duration:.3f}s)")
            
            # Log to audit service
            self.audit_service.log_access(
                principal=user_principal,
                resource=request.url.path,
                action=request.method.lower(),
                outcome="success" if response.status_code < 400 else "error",
                details=f"Status: {response.status_code}, Duration: {duration:.3f}s",
                ip_address=client_ip
            )
            
            return response
            
        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time
            
            # Log the exception
            logger.error(f"Exception: {str(e)} for {request.method} {request.url.path} (Duration: {duration:.3f}s)")
            
            # Log to audit service
            self.audit_service.log_access(
                principal=user_principal,
                resource=request.url.path,
                action=request.method.lower(),
                outcome="error",
                details=f"Exception: {str(e)}, Duration: {duration:.3f}s",
                ip_address=client_ip
            )
            
            # Re-raise the exception
            raise