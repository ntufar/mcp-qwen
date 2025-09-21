from typing import List, Dict, Any
from src.models.access_policy import AccessPolicyModel
from src.models.user_session import UserSessionModel
import fnmatch
from datetime import datetime

class AccessControlService:
    def __init__(self):
        self.policies: List[AccessPolicyModel] = []
    
    def add_policy(self, policy: AccessPolicyModel) -> None:
        """
        Add an access policy.
        
        Args:
            policy: AccessPolicyModel to add
        """
        self.policies.append(policy)
    
    def check_access(self, user_session: UserSessionModel, resource: str, action: str) -> bool:
        """
        Check if a user has access to a resource for a specific action.
        
        Args:
            user_session: UserSessionModel for the user
            resource: Resource path to check access for
            action: Action to check access for (read, list, search, etc.)
            
        Returns:
            True if access is granted, False otherwise
        """
        # Check each policy
        for policy in self.policies:
            # Check if the user matches the policy principals
            if self._matches_principal(user_session.principal, policy.principals):
                # Check if the resource matches the policy resources
                if self._matches_resource(resource, policy.resources):
                    # Check if the action is allowed
                    if action in policy.actions:
                        # Check conditions if any
                        if self._check_conditions(policy.conditions, user_session.metadata):
                            return True
        return False
    
    def _matches_principal(self, principal: str, principals: List[str]) -> bool:
        """
        Check if a principal matches any of the policy principals.
        
        Args:
            principal: Principal to check
            principals: List of policy principals (can include wildcards)
            
        Returns:
            True if principal matches, False otherwise
        """
        for policy_principal in principals:
            if fnmatch.fnmatch(principal, policy_principal):
                return True
        return False
    
    def _matches_resource(self, resource: str, resources: List[str]) -> bool:
        """
        Check if a resource matches any of the policy resources.
        
        Args:
            resource: Resource path to check
            resources: List of policy resources (can include wildcards)
            
        Returns:
            True if resource matches, False otherwise
        """
        for policy_resource in resources:
            if fnmatch.fnmatch(resource, policy_resource):
                return True
        return False
    
    def _check_conditions(self, conditions: Dict[str, Any], metadata: Dict[str, Any]) -> bool:
        """
        Check if all conditions are met.
        
        Args:
            conditions: Policy conditions to check
            metadata: User session metadata
            
        Returns:
            True if all conditions are met, False otherwise
        """
        # For now, we'll implement a simple check
        # In a real implementation, this would be more complex
        for key, value in conditions.items():
            if key in metadata:
                if metadata[key] != value:
                    return False
            else:
                # If condition key is not in metadata, condition is not met
                return False
        return True