import os
import pathlib
from typing import List, Union
from src.models.directory import DirectoryModel
from src.models.file import FileModel
from src.services.file_service import FileService
from src.utils.path_validator import validate_path
from src.utils.directory_cache import directory_cache
from datetime import datetime
import stat
import hashlib
from src.config import settings

class DirectoryService:
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
    def _create_relative_path(absolute_path: pathlib.Path) -> str:
        """
        Create a relative path from an absolute path within allowed directories.
        
        Args:
            absolute_path: Absolute path to convert to relative
            
        Returns:
            Relative path within allowed directories
        """
        # Try each allowed directory
        for allowed_dir in settings.ALLOWED_DIRECTORIES:
            resolved_allowed_dir = pathlib.Path(allowed_dir).resolve()
            
            # Check if absolute_path is within resolved_allowed_dir
            try:
                relative_path = absolute_path.relative_to(resolved_allowed_dir)
                return str(relative_path)
            except ValueError:
                # absolute_path is not within resolved_allowed_dir
                continue
        
        # If we get here, the path is not within any allowed directory
        raise ValueError(f"Path not within allowed directories: {absolute_path}")
    
    @staticmethod
    def get_directory_info(dir_path: str) -> DirectoryModel:
        """
        Get information about a directory.
        
        Args:
            dir_path: Path to the directory
            
        Returns:
            DirectoryModel with directory information
        """
        # Validate path
        if not validate_path(dir_path):
            raise ValueError("Invalid directory path")
        
        # Create cache key
        cache_key = hashlib.md5(dir_path.encode()).hexdigest()
        
        # Try to get from cache first
        cached_result = directory_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Resolve the path
        path = DirectoryService._resolve_path(dir_path)
        stat_info = path.stat()
        
        # Get contents (files and subdirectories)
        contents = []
        if path.is_dir():
            try:
                for item in path.iterdir():
                    if item.is_file():
                        # Create a relative path for the file
                        relative_item_path = DirectoryService._create_relative_path(item)
                        contents.append(FileService.get_file_info(relative_item_path))
                    elif item.is_dir():
                        # Create a relative path for the directory
                        relative_item_path = DirectoryService._create_relative_path(item)
                        contents.append(DirectoryService.get_directory_info(relative_item_path))
            except PermissionError:
                # Handle permission errors gracefully
                pass
        
        # Use the original path for the path field to match expectations
        original_full_path = os.path.join(settings.ALLOWED_DIRECTORIES[0], dir_path)
        
        result = DirectoryModel(
            id=str(hash(dir_path)),
            name=path.name,
            path=original_full_path,  # Use original path
            size=stat_info.st_size,
            modified_at=datetime.fromtimestamp(stat_info.st_mtime),
            created_at=datetime.fromtimestamp(stat_info.st_ctime),
            permissions=stat.filemode(stat_info.st_mode),
            contents=contents
        )
        
        # Cache the result
        directory_cache.set(cache_key, result)
        
        return result
    
    @staticmethod
    def list_directory_contents(dir_path: str, limit: int = 100, offset: int = 0) -> List[Union[FileModel, DirectoryModel]]:
        """
        List the contents of a directory with pagination.
        
        Args:
            dir_path: Path to the directory
            limit: Maximum number of items to return
            offset: Number of items to skip
            
        Returns:
            List of FileModel and DirectoryModel objects
        """
        # Validate path
        if not validate_path(dir_path):
            raise ValueError("Invalid directory path")
        
        # Resolve the path
        path = DirectoryService._resolve_path(dir_path)
        contents = []
        
        if path.is_dir():
            try:
                items = list(path.iterdir())
                # Apply pagination
                paginated_items = items[offset:offset + limit]
                
                for item in paginated_items:
                    if item.is_file():
                        # Create a relative path for the file
                        relative_item_path = DirectoryService._create_relative_path(item)
                        contents.append(FileService.get_file_info(relative_item_path))
                    elif item.is_dir():
                        # For directory listings, we typically don't include full contents
                        # to avoid performance issues. We just include basic info.
                        stat_info = item.stat()
                        # Create a relative path for the directory
                        relative_item_path = DirectoryService._create_relative_path(item)
                        contents.append(DirectoryModel(
                            id=str(hash(relative_item_path)),
                            name=item.name,
                            path=str(item),  # Use the original path
                            size=stat_info.st_size,
                            modified_at=datetime.fromtimestamp(stat_info.st_mtime),
                            created_at=datetime.fromtimestamp(stat_info.st_ctime),
                            permissions=stat.filemode(stat_info.st_mode),
                            contents=[]  # Empty for performance
                        ))
            except PermissionError:
                # Handle permission errors gracefully
                pass
                
        return contents
    
    @staticmethod
    def directory_exists(dir_path: str) -> bool:
        """
        Check if a directory exists.
        
        Args:
            dir_path: Path to the directory
            
        Returns:
            True if directory exists, False otherwise
        """
        # Validate path
        if not validate_path(dir_path):
            return False
            
        try:
            path = DirectoryService._resolve_path(dir_path)
            return path.is_dir()
        except FileNotFoundError:
            return False