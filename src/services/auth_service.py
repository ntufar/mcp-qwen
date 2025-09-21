from typing import Optional
from src.models.user_session import UserSessionModel
from datetime import datetime, timedelta
import secrets

class AuthService:
    def __init__(self):
        self.sessions = {}  # In a real implementation, this would be a database
    
    def create_session(self, principal: str, scopes: list, duration_hours: int = 24) -> UserSessionModel:
        """
        Create a new user session.
        
        Args:
            principal: User identifier
            scopes: List of access scopes
            duration_hours: Session duration in hours (default: 24)
            
        Returns:
            UserSessionModel with session information
        """
        # Generate a random token
        token = secrets.token_urlsafe(32)
        
        # Create session
        session = UserSessionModel(
            id=str(hash(token)),
            token=token,
            principal=principal,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=duration_hours),
            scopes=scopes,
            metadata={}
        )
        
        # Store session
        self.sessions[token] = session
        
        return session
    
    def validate_session(self, token: str) -> Optional[UserSessionModel]:
        """
        Validate a session token.
        
        Args:
            token: Session token to validate
            
        Returns:
            UserSessionModel if valid, None if invalid or expired
        """
        if token in self.sessions:
            session = self.sessions[token]
            # Check if session is expired
            if session.expires_at > datetime.now():
                return session
            else:
                # Remove expired session
                del self.sessions[token]
        return None
    
    def revoke_session(self, token: str) -> bool:
        """
        Revoke a session.
        
        Args:
            token: Session token to revoke
            
        Returns:
            True if session was revoked, False if not found
        """
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False