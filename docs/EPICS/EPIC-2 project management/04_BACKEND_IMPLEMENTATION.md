# EPIC-02 — Project Workspace Management

## 04_BACKEND_IMPLEMENTATION.md

---

# Document Information

| Property | Value |
|----------|-------|
| Project | Privacy-Preserving Synthetic HR Records Generator |
| Epic | EPIC-02 |
| Document | Backend Implementation Guide |
| Version | 1.0.0 |
| Status | Draft |
| Depends On | 03_DATABASE_DESIGN.md |

---

# 1. Purpose

This document defines the backend implementation strategy for **EPIC-02 – Project Workspace Management**.

It specifies the Django application structure, models, serializers, services, permissions, API views, validators, exceptions, and implementation order.

The objective is to ensure that all business logic remains modular, testable, secure, and production-ready.

---

# 2. Technology Stack

Backend Framework

- Django

API Framework

- Django REST Framework

Database

- PostgreSQL

Authentication

- JWT Authentication

Background Tasks (Future)

- Celery

Message Broker (Future)

- Redis

---

# 3. Django Application

```
apps/

projects/

├── migrations/
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── services.py
├── permissions.py
├── validators.py
├── exceptions.py
├── urls.py
├── views.py
├── signals.py
├── managers.py
├── filters.py
├── utils.py
└── tests/
```

---

# 4. Responsibilities

The Project application is responsible for:

- Project lifecycle
- Ownership
- Dashboard statistics
- Project metadata
- Project authorization
- Search
- Filtering
- Ordering

The Project application shall not manage:

- Datasets
- Schemas
- AI Models
- Differential Privacy
- Exports

---

# 5. Models

## Project

Responsibilities

- Store project information
- Maintain ownership
- Maintain lifecycle
- Support future relationships

---

# 6. Managers

Create:

## ProjectManager

Responsibilities

- Active projects
- Archived projects
- Deleted projects
- Owner filtering

---

# 7. Serializers

Create:

---

## ProjectCreateSerializer

Responsibilities

- Validate input
- Create project
- Generate slug
- Return response

---

## ProjectUpdateSerializer

Responsibilities

- Update editable fields
- Validate updates

---

## ProjectDetailSerializer

Responsibilities

Return complete project information.

---

## ProjectListSerializer

Responsibilities

Optimized serializer for project listing.

---

## DashboardSerializer

Responsibilities

Return dashboard statistics.

---

# 8. Service Layer

Business logic belongs here.

Create:

---

## ProjectService

Responsibilities

- Create project
- Update project
- Archive project
- Restore project
- Delete project
- Retrieve project
- List projects

---

## DashboardService

Responsibilities

- Dashboard statistics
- Future integrations
- Summary generation

---

## OwnershipService

Responsibilities

- Validate ownership
- Permission checks

---

# 9. API Views

Views remain thin.

Create:

```
ProjectListCreateAPIView

ProjectDetailAPIView

ProjectUpdateAPIView

ProjectDeleteAPIView

ProjectArchiveAPIView

ProjectRestoreAPIView

DashboardAPIView
```

Views shall:

- Validate request
- Call services
- Return standardized responses

Views shall never contain business logic.

---

# 10. Permissions

Create custom permissions.

Examples

```
IsProjectOwner

CanArchiveProject

CanRestoreProject

CanDeleteProject
```

All permissions must inherit from DRF BasePermission.

---

# 11. Validators

Reusable validators.

Examples

```
ProjectNameValidator

ProjectStatusValidator

ProjectSlugValidator
```

Validators should never perform business workflows.

---

# 12. Exceptions

Create custom exceptions.

Examples

```
ProjectNotFoundException

DuplicateProjectException

ProjectAlreadyArchivedException

ProjectAlreadyDeletedException

UnauthorizedProjectAccessException

InvalidProjectStateException
```

Business exceptions remain separate from framework exceptions.

---

# 13. Filters

Support

- Search
- Ordering
- Status
- Date range

Use django-filter.

---

# 14. URLs

```
/projects/

/projects/<uuid:id>/

/projects/<uuid:id>/archive/

/projects/<uuid:id>/restore/

/projects/dashboard/
```

Versioning handled at API root.

---

# 15. Request Flow

```
Request

↓

APIView

↓

Serializer Validation

↓

Permission Check

↓

Project Service

↓

Database

↓

Serializer

↓

Response
```

---

# 16. Business Rules

The backend shall enforce:

- Authentication required
- Ownership validation
- Soft deletion
- Unique names per owner
- Valid lifecycle transitions

---

# 17. Signals

Signals only for side effects.

Examples

- Audit log
- Cache invalidation (future)
- Notifications (future)

Business logic shall never exist inside signals.

---

# 18. Logging

Log

- Project Created
- Project Updated
- Project Archived
- Project Restored
- Project Deleted
- Unauthorized Access
- Validation Failures

Never log confidential information.

---

# 19. Transactions

Database transactions required for:

- Create
- Update
- Archive
- Restore
- Delete

Use:

```
transaction.atomic()
```

where multiple database operations occur.

---

# 20. Error Handling

Errors must be

- Structured
- Consistent
- Logged
- Traceable

API response example

```json
{
    "success": false,
    "message": "Project already exists.",
    "error_code": "PROJECT_EXISTS"
}
```

---

# 21. Security

The backend shall implement

- JWT Authentication
- Object-level permissions
- Ownership validation
- Input validation
- Secure responses
- Rate limiting (Future)

---

# 22. Performance

Implementation should support

- Pagination
- Optimized ORM queries
- Database indexes
- Lazy loading where appropriate
- Future caching

Avoid N+1 query problems.

---

# 23. Testing Requirements

Backend tests shall cover

Models

- Project model

Managers

- Active manager
- Deleted manager

Serializers

- Create
- Update
- Validation

Services

- CRUD
- Dashboard
- Authorization

Views

- All endpoints

Permissions

- Owner
- Non-owner

Validation

- Duplicate names
- Status
- Ownership

Integration

- Complete project lifecycle

---

# 24. Implementation Order

### Phase 1

- Create Django app
- Register app
- Create Project model

---

### Phase 2

- Managers
- Validators
- Exceptions

---

### Phase 3

- Serializers

---

### Phase 4

- Services

---

### Phase 5

- Permissions

---

### Phase 6

- API Views
- URLs

---

### Phase 7

- Dashboard
- Search
- Filters
- Ordering

---

### Phase 8

- Logging
- Signals

---

### Phase 9

- Testing
- Documentation
- Code Review

---

# 25. Deliverables

At completion the backend provides

- Project CRUD
- Ownership validation
- Dashboard
- Search
- Filtering
- Ordering
- Archive
- Restore
- Soft Delete
- Logging
- Production-ready APIs

---

# 26. Definition of Done

Backend implementation is complete when

- APIs functional
- Services implemented
- Permissions implemented
- Validation completed
- Tests passing
- Documentation updated
- Security review completed
- Code review approved

---

# 27. Related Documents

- 00_EPIC_OVERVIEW.md
- 01_FEATURE_BREAKDOWN.md
- 02_USER_STORIES.md
- 03_DATABASE_DESIGN.md
- 05_FRONTEND_IMPLEMENTATION.md
- 06_API_IMPLEMENTATION.md
- 07_SECURITY_IMPLEMENTATION.md
- 08_TESTING_PLAN.md

---

# Version History

| Version | Description |
|----------|-------------|
| 1.0.0 | Initial backend implementation guide for EPIC-02 |