import os
import pathlib
from typing import List, Optional
from src.models.file import FileModel
from src.utils.path_validator import validate_path
from datetime import datetime
import stat
from src.config import settings

class FileService:
    @staticmethod
    def _resolve_path(relative_path: str) -> pathlib.Path:
        """
        Resolve a relative path to an absolute path within allowed directories.
        
        Args:
            relative_path: Relative path to resolve
            
        Returns:
            Absolute path within allowed directories
        """
        # Try each allowed directory
        for allowed_dir in settings.ALLOWED_DIRECTORIES:
            full_path = os.path.join(allowed_dir, relative_path)
            resolved_path = pathlib.Path(full_path).resolve()
            resolved_allowed_dir = pathlib.Path(allowed_dir).resolve()
            
            # Check if resolved_path is within resolved_allowed_dir
            try:
                resolved_path.relative_to(resolved_allowed_dir)
                if resolved_path.exists():
                    return resolved_path
            except ValueError:
                # resolved_path is not within resolved_allowed_dir
                continue
        
        # If we get here, the path is not within any allowed directory or doesn't exist
        raise FileNotFoundError(f"Path not found within allowed directories: {relative_path}")
    
    @staticmethod
    def get_file_info(file_path: str) -> FileModel:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileModel with file information
        """
        # Validate path
        if not validate_path(file_path):
            raise ValueError("Invalid file path")
        
        # Resolve the path
        path = FileService._resolve_path(file_path)
        stat_info = path.stat()
        
        # Use the original path for the path field to match expectations
        original_full_path = os.path.join(settings.ALLOWED_DIRECTORIES[0], file_path)
        
        return FileModel(
            id=str(hash(file_path)),
            name=path.name,
            path=original_full_path,  # Use original path
            size=stat_info.st_size,
            type=path.suffix,
            modified_at=datetime.fromtimestamp(stat_info.st_mtime),
            created_at=datetime.fromtimestamp(stat_info.st_ctime),
            permissions=stat.filemode(stat_info.st_mode)
        )
    
    @staticmethod
    def read_file_content(file_path: str, encoding: str = "utf-8", limit: int = 10485760) -> str:
        """
        Read the content of a file.
        
        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)
            limit: Maximum number of bytes to read (default: 10MB)
            
        Returns:
            File content as string
        """
        # Validate path
        if not validate_path(file_path):
            raise ValueError("Invalid file path")
        
        # Resolve the path
        path = FileService._resolve_path(file_path)
        
        # Check file size
        if path.stat().st_size > limit:
            raise ValueError(f"File size exceeds limit of {limit} bytes")
        
        with open(path, "r", encoding=encoding) as file:
            # Read up to limit bytes
            content = file.read(limit)
            return content
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file exists, False otherwise
        """
        # Validate path
        if not validate_path(file_path):
            return False
            
        try:
            path = FileService._resolve_path(file_path)
            return path.is_file()
        except FileNotFoundError:
            return False