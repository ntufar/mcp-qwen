from functools import lru_cache
import time
from typing import Dict, Any, Optional

class DirectoryCache:
    def __init__(self, maxsize: int = 128, ttl: int = 300):
        """
        Initialize the directory cache.
        
        Args:
            maxsize: Maximum number of entries in the cache
            ttl: Time to live in seconds
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.access_times: Dict[str, float] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        if key not in self.cache:
            return None
        
        # Check if entry is expired
        if time.time() - self.access_times[key] > self.ttl:
            # Remove expired entry
            del self.cache[key]
            del self.access_times[key]
            return None
        
        # Update access time
        self.access_times[key] = time.time()
        return self.cache[key]["value"]
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        # If cache is at max size, remove oldest entry
        if len(self.cache) >= self.maxsize:
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        # Add new entry
        self.cache[key] = {"value": value}
        self.access_times[key] = time.time()
    
    def clear(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        self.access_times.clear()

# Global directory cache instance
directory_cache = DirectoryCache()