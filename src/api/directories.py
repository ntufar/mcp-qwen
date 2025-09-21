from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Union
from src.models.directory import DirectoryModel
from src.models.file import FileModel
from src.services.directory_service import DirectoryService
from src.services.auth_service import AuthService
from src.services.access_control_service import AccessControlService
from src.services.audit_service import AuditService
from src.models.user_session import UserSessionModel
from src.utils.error_handler import handle_directory_not_found, handle_permission_denied, handle_internal_error

router = APIRouter()

# Initialize services
auth_service = AuthService()
access_control_service = AccessControlService()
audit_service = AuditService()
directory_service = DirectoryService()

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

class DirectoryResponse(DirectoryModel):
    contents: List[Union[FileModel, DirectoryModel]]
    total_count: int
    has_more: bool

@router.get("/directories/{path:path}", response_model=DirectoryResponse)
async def list_directory(
    path: str,
    recursive: bool = Query(False, description="Whether to list contents recursively"),
    limit: int = Query(100, description="Maximum number of items to return", ge=1, le=1000),
    offset: int = Query(0, description="Number of items to skip", ge=0),
    user: UserSessionModel = Depends(get_current_user)
):
    """
    List the contents of a directory.
    
    Args:
        path: Path to the directory
        recursive: Whether to list contents recursively
        limit: Maximum number of items to return
        offset: Number of items to skip
        user: Current user session (from authorization header)
        
    Returns:
        DirectoryResponse with directory information and contents
    """
    # Log the access attempt
    audit_service.log_access(
        principal=user.principal,
        resource=f"directory:{path}",
        action="list",
        outcome="attempt",
        details=f"recursive={recursive}, limit={limit}, offset={offset}"
    )
    
    # Check access control
    if not access_control_service.check_access(user, f"directory:{path}", "list"):
        audit_service.log_access(
            principal=user.principal,
            resource=f"directory:{path}",
            action="list",
            outcome="denied",
            details=f"Access denied for directory:{path}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Check if directory exists
    if not directory_service.directory_exists(path):
        audit_service.log_access(
            principal=user.principal,
            resource=f"directory:{path}",
            action="list",
            outcome="error",
            details=f"Directory not found: {path}"
        )
        handle_directory_not_found(path)
    
    # Get directory information
    try:
        directory_info = directory_service.get_directory_info(path)
        
        # If recursive is False, get paginated contents
        if not recursive:
            contents = directory_service.list_directory_contents(path, limit, offset)
            total_count = len(directory_info.contents) if directory_info.contents else 0
            has_more = total_count > offset + limit
            
            # Update the response with paginated contents
            response = DirectoryResponse(
                id=directory_info.id,
                name=directory_info.name,
                path=directory_info.path,
                size=directory_info.size,
                modified_at=directory_info.modified_at,
                created_at=directory_info.created_at,
                permissions=directory_info.permissions,
                contents=contents,
                total_count=total_count,
                has_more=has_more
            )
        else:
            # For recursive listing, return all contents
            response = DirectoryResponse(
                id=directory_info.id,
                name=directory_info.name,
                path=directory_info.path,
                size=directory_info.size,
                modified_at=directory_info.modified_at,
                created_at=directory_info.created_at,
                permissions=directory_info.permissions,
                contents=directory_info.contents,
                total_count=len(directory_info.contents) if directory_info.contents else 0,
                has_more=False
            )
        
        # Log successful access
        audit_service.log_access(
            principal=user.principal,
            resource=f"directory:{path}",
            action="list",
            outcome="success",
            details=f"Listed directory with {len(response.contents)} items"
        )
        
        return response
        
    except PermissionError:
        audit_service.log_access(
            principal=user.principal,
            resource=f"directory:{path}",
            action="list",
            outcome="error",
            details=f"Permission denied for directory: {path}"
        )
        handle_permission_denied(path)
    except Exception as e:
        audit_service.log_access(
            principal=user.principal,
            resource=f"directory:{path}",
            action="list",
            outcome="error",
            details=f"Error listing directory: {str(e)}"
        )
        handle_internal_error(e)