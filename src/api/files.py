from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
import pathlib
from src.services.file_service import FileService
from src.services.auth_service import AuthService
from src.services.access_control_service import AccessControlService
from src.services.audit_service import AuditService
from src.models.user_session import UserSessionModel
from src.utils.error_handler import handle_file_not_found, handle_permission_denied, handle_internal_error, handle_file_too_large

router = APIRouter()

# Initialize services
auth_service = AuthService()
access_control_service = AccessControlService()
audit_service = AuditService()
file_service = FileService()

def get_current_user(authorization: str = None) -> UserSessionModel:
    """Dependency to get current user from authorization header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Extract token from "Bearer <token>" format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme"
        )
    
    token = authorization[7:]  # Remove "Bearer " prefix
    user_session = auth_service.validate_session(token)
    
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user_session

@router.get("/files/{path:path}", response_class=str)
async def read_file(
    path: str,
    encoding: str = Query("utf-8", description="File encoding"),
    limit: int = Query(10485760, description="Maximum number of bytes to read (default: 10MB)", ge=1, le=104857600),
    user: UserSessionModel = Depends(get_current_user)
):
    """
    Read the contents of a file.
    
    Args:
        path: Path to the file
        encoding: File encoding (default: utf-8)
        limit: Maximum number of bytes to read (default: 10MB)
        user: Current user session (from authorization header)
        
    Returns:
        File content as string
    """
    # Log the access attempt
    audit_service.log_access(
        principal=user.principal,
        resource=f"file:{path}",
        action="read",
        outcome="attempt",
        details=f"encoding={encoding}, limit={limit}"
    )
    
    # Check access control
    if not access_control_service.check_access(user, f"file:{path}", "read"):
        audit_service.log_access(
            principal=user.principal,
            resource=f"file:{path}",
            action="read",
            outcome="denied",
            details=f"Access denied for file:{path}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Check if file exists
    if not file_service.file_exists(path):
        audit_service.log_access(
            principal=user.principal,
            resource=f"file:{path}",
            action="read",
            outcome="error",
            details=f"File not found: {path}"
        )
        handle_file_not_found(path)
    
    # Read file content
    try:
        content = file_service.read_file_content(path, encoding, limit)
        
        # Log successful access
        audit_service.log_access(
            principal=user.principal,
            resource=f"file:{path}",
            action="read",
            outcome="success",
            details=f"Read {len(content)} characters from file"
        )
        
        return content
        
    except PermissionError:
        audit_service.log_access(
            principal=user.principal,
            resource=f"file:{path}",
            action="read",
            outcome="error",
            details=f"Permission denied for file: {path}"
        )
        handle_permission_denied(path)
    except UnicodeDecodeError:
        audit_service.log_access(
            principal=user.principal,
            resource=f"file:{path}",
            action="read",
            outcome="error",
            details=f"Unable to decode file with encoding: {encoding}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to decode file with encoding: {encoding}"
        )
    except ValueError as e:
        if "exceeds limit" in str(e):
            # Handle file too large error
            try:
                file_size = pathlib.Path(path).stat().st_size
                audit_service.log_access(
                    principal=user.principal,
                    resource=f"file:{path}",
                    action="read",
                    outcome="error",
                    details=f"File too large: {file_size} bytes, limit: {limit} bytes"
                )
                handle_file_too_large(path, file_size, limit)
            except:
                handle_internal_error(e)
        else:
            audit_service.log_access(
                principal=user.principal,
                resource=f"file:{path}",
                action="read",
                outcome="error",
                details=f"Error reading file: {str(e)}"
            )
            handle_internal_error(e)
    except Exception as e:
        audit_service.log_access(
            principal=user.principal,
            resource=f"file:{path}",
            action="read",
            outcome="error",
            details=f"Error reading file: {str(e)}"
        )
        handle_internal_error(e)