# Tasks: MCP Server for LLM File Browsing

**Input**: Design documents from `/specs/001-project-to-create/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [x] T001 Create project structure per implementation plan
- [x] T002 Initialize Python project with FastAPI dependencies
- [x] T003 [P] Configure linting and formatting tools (black, flake8, isort)
- [x] T004 [P] Create requirements.txt with FastAPI, Pydantic, pytest, and other dependencies
- [x] T005 [P] Set up project configuration files (.env.example, config.py)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T006 [P] Contract test GET /directories/{path} in tests/contract/test_list_directory.py
- [x] T007 [P] Contract test GET /files/{path} in tests/contract/test_read_file.py
- [x] T008 [P] Integration test directory listing in tests/integration/test_directory_listing.py
- [x] T009 [P] Integration test file reading in tests/integration/test_file_reading.py
- [x] T010 [P] Integration test access control in tests/integration/test_access_control.py
- [x] T011 [P] Integration test authentication in tests/integration/test_authentication.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T012 [P] File model in src/models/file.py
- [x] T013 [P] Directory model in src/models/directory.py
- [x] T014 [P] AccessPolicy model in src/models/access_policy.py
- [x] T015 [P] AuditLog model in src/models/audit_log.py
- [x] T016 [P] UserSession model in src/models/user_session.py
- [x] T017 [P] FileService in src/services/file_service.py
- [x] T018 [P] DirectoryService in src/services/directory_service.py
- [x] T019 [P] AccessControlService in src/services/access_control_service.py
- [x] T020 [P] AuditService in src/services/audit_service.py
- [x] T021 [P] AuthService in src/services/auth_service.py
- [x] T022 GET /directories/{path} endpoint in src/api/directories.py
- [x] T023 GET /files/{path} endpoint in src/api/files.py
- [x] T024 Input validation for path parameters
- [x] T025 Error handling and logging

## Phase 3.4: Integration
- [x] T026 Configure OAuth2 authentication middleware
- [x] T027 Implement access control middleware
- [x] T028 Set up audit logging middleware
- [x] T029 Configure file system access limits
- [x] T030 Implement caching for directory listings

## Phase 3.5: Polish
- [x] T031 [P] Unit tests for File model in tests/unit/test_file_model.py
- [x] T032 [P] Unit tests for Directory model in tests/unit/test_directory_model.py
- [x] T033 [P] Unit tests for AccessPolicy model in tests/unit/test_access_policy_model.py
- [x] T034 [P] Unit tests for AuditLog model in tests/unit/test_audit_log_model.py
- [x] T035 [P] Unit tests for UserSession model in tests/unit/test_user_session_model.py
- [x] T036 [P] Unit tests for FileService in tests/unit/test_file_service.py
- [x] T037 [P] Unit tests for DirectoryService in tests/unit/test_directory_service.py
- [x] T038 Performance tests (<100ms response time)
- [x] T039 [P] Update docs/api.md with endpoint documentation
- [x] T040 [P] Update docs/security.md with security implementation details
- [x] T041 Update README.md with project overview and usage instructions
- [x] T042 Run manual-testing.md to validate quickstart guide

## Dependencies
- Tests (T006-T011) before implementation (T012-T025)
- Model tasks (T012-T016) before service tasks (T017-T021)
- Service tasks (T017-T021) before endpoint tasks (T022-T023)
- Core implementation (T012-T025) before integration (T026-T030)
- Integration (T026-T030) before polish (T031-T042)

## Parallel Example
```
# Launch T006-T011 together:
Task: "Contract test GET /directories/{path} in tests/contract/test_list_directory.py"
Task: "Contract test GET /files/{path} in tests/contract/test_read_file.py"
Task: "Integration test directory listing in tests/integration/test_directory_listing.py"
Task: "Integration test file reading in tests/integration/test_file_reading.py"
Task: "Integration test access control in tests/integration/test_access_control.py"
Task: "Integration test authentication in tests/integration/test_authentication.py"

# Launch T012-T016 together:
Task: "File model in src/models/file.py"
Task: "Directory model in src/models/directory.py"
Task: "AccessPolicy model in src/models/access_policy.py"
Task: "AuditLog model in src/models/audit_log.py"
Task: "UserSession model in src/models/user_session.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests
- [x] All entities have model tasks
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task