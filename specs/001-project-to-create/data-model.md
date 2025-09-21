# Data Model: MCP Server for LLM File Browsing

## Entities

### File
Represents a file in the file system.

**Attributes**:
- id: str (unique identifier)
- name: str (file name)
- path: str (full path to file)
- size: int (file size in bytes)
- type: str (file extension or MIME type)
- modified_at: datetime (last modification timestamp)
- created_at: datetime (creation timestamp)
- permissions: str (file permissions in symbolic form)

### Directory
Represents a directory in the file system.

**Attributes**:
- id: str (unique identifier)
- name: str (directory name)
- path: str (full path to directory)
- size: int (total size of directory contents in bytes)
- modified_at: datetime (last modification timestamp)
- created_at: datetime (creation timestamp)
- permissions: str (directory permissions in symbolic form)
- contents: List[Union[File, Directory]] (items contained in the directory)

### AccessPolicy
Represents the rules governing which LLMs can access which files/directories.

**Attributes**:
- id: str (unique identifier)
- name: str (policy name)
- description: str (policy description)
- resources: List[str] (paths or patterns this policy applies to)
- principals: List[str] (LLM identifiers or groups this policy applies to)
- actions: List[str] (allowed actions: read, list, search)
- conditions: Dict[str, Any] (additional conditions for access)
- created_at: datetime (creation timestamp)
- updated_at: datetime (last update timestamp)

### AuditLog
Represents a record of file access attempts.

**Attributes**:
- id: str (unique identifier)
- timestamp: datetime (when the access attempt occurred)
- principal: str (LLM identifier)
- resource: str (file or directory path)
- action: str (operation attempted: read, list, search)
- outcome: str (success, denied, error)
- details: str (additional information about the attempt)
- ip_address: str (IP address of the requesting LLM)

### UserSession
Represents an authenticated session for an LLM.

**Attributes**:
- id: str (unique identifier)
- token: str (session token)
- principal: str (LLM identifier)
- created_at: datetime (session creation timestamp)
- expires_at: datetime (session expiration timestamp)
- scopes: List[str] (access scopes granted to this session)
- metadata: Dict[str, Any] (additional session information)

## Relationships

1. **Directory** contains **File** and **Directory** (hierarchical relationship)
2. **AccessPolicy** governs access to **File** and **Directory**
3. **AuditLog** records interactions with **File** and **Directory**
4. **UserSession** is associated with **AccessPolicy** through scopes

## Validation Rules

### File
- path must be a valid file path
- size must be non-negative
- type must be a valid file type or extension

### Directory
- path must be a valid directory path
- contents must only contain File or Directory objects

### AccessPolicy
- resources must be valid path patterns
- principals must be valid LLM identifiers
- actions must be from the allowed set: read, list, search

### AuditLog
- timestamp must be in the past
- outcome must be from the allowed set: success, denied, error
- resource must be a valid path

### UserSession
- expires_at must be after created_at
- scopes must be from the allowed set defined by the system