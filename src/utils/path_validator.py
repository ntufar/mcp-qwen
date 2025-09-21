import re
import os
from pathlib import Path
from src.config import settings

def validate_path(path: str) -> bool:
    """
    Validate a file or directory path.
    
    Args:
        path: Path to validate
        
    Returns:
        True if path is valid, False otherwise
    """
    # Check if path is empty
    if not path:
        return False
    
    # Check for invalid characters (Windows-specific)
    if re.search(r'[<>:"|?*]', path):
        return False
    
    # Check if path is absolute
    if os.path.isabs(path):
        # For security, we don't allow absolute paths
        return False
    
    # Check if the path is within allowed directories
    for allowed_dir in settings.ALLOWED_DIRECTORIES:
        # Create the full path by joining the allowed directory with the relative path
        full_path = os.path.join(allowed_dir, path)
        
        # Resolve the full path to handle any '..' or '.' components
        try:
            resolved_full_path = Path(full_path).resolve()
            resolved_allowed_dir = Path(allowed_dir).resolve()
            
            # Check if resolved_full_path is within resolved_allowed_dir
            try:
                resolved_full_path.relative_to(resolved_allowed_dir)
                # Check if the path actually exists
                if os.path.exists(resolved_full_path):
                    return True
            except ValueError:
                # resolved_full_path is not within resolved_allowed_dir
                continue
        except Exception:
            # If there's any error resolving the path, continue checking
            continue
    
    # If we get here, the path is not within any allowed directory or doesn't exist
    return False

def sanitize_path(path: str) -> str:
    """
    Sanitize a path by removing potentially dangerous characters.
    
    Args:
        path: Path to sanitize
        
    Returns:
        Sanitized path
    """
    # Remove null bytes
    path = path.replace('\x00', '')
    
    # Remove control characters
    path = ''.join(char for char in path if ord(char) >= 32)
    
    return path