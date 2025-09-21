from fastapi import HTTPException, status
from typing import Optional
import logging

# Set up logging
logger = logging.getLogger("mcp_server")
logger.setLevel(logging.INFO)

class MCPException(HTTPException):
    """Custom exception class for MCP Server"""
    
    def __init__(self, status_code: int, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

def handle_file_not_found(path: str) -> None:
    """Handle file not found errors"""
    logger.warning(f"File not found: {path}")
    raise MCPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="File not found",
        error_code="FILE_NOT_FOUND"
    )

def handle_directory_not_found(path: str) -> None:
    """Handle directory not found errors"""
    logger.warning(f"Directory not found: {path}")
    raise MCPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Directory not found",
        error_code="DIRECTORY_NOT_FOUND"
    )

def handle_permission_denied(path: str) -> None:
    """Handle permission denied errors"""
    logger.warning(f"Permission denied: {path}")
    raise MCPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied",
        error_code="ACCESS_DENIED"
    )

def handle_file_too_large(path: str, size: int, limit: int) -> None:
    """Handle file too large errors"""
    logger.warning(f"File too large: {path} ({size} bytes, limit: {limit} bytes)")
    raise MCPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail="File too large",
        error_code="FILE_TOO_LARGE"
    )

def handle_invalid_path(path: str) -> None:
    """Handle invalid path errors"""
    logger.warning(f"Invalid path: {path}")
    raise MCPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid path",
        error_code="INVALID_PATH"
    )

def handle_internal_error(error: Exception) -> None:
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    raise MCPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error",
        error_code="INTERNAL_ERROR"
    )