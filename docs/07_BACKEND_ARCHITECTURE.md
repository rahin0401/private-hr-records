# 07_BACKEND_ARCHITECTURE.md

**Project:** Privacy-Preserving Synthetic HR Records Generator
**Document:** Backend Architecture
**Version:** 1.0.0
**Status:** Draft
**Depends On:** 03_SYSTEM_ARCHITECTURE.md, 04_AI_ARCHITECTURE.md, 06_DATA_GENERATION_PIPELINE.md

---

# 1. Purpose

This document defines the backend architecture of the Privacy-Preserving Synthetic HR Records Generator.

It specifies the organization of the backend codebase, module responsibilities, dependency rules, service boundaries, and implementation guidelines.

---

# 2. Technology Stack

Backend Framework:

* Django

API Framework:

* Django REST Framework (DRF)

Database:

* PostgreSQL

Authentication:

* JWT Authentication

Background Processing:

* Celery (Future)

Message Broker:

* Redis (Future)

Storage:

* Local Storage (Development)
* Cloud Storage (Future)

---

# 3. Architectural Principles

The backend follows:

* Clean Architecture
* SOLID Principles
* DRY
* Separation of Concerns
* Service-Oriented Business Logic
* Modular Applications
* API-First Design
* Dependency Inversion

---

# 4. Backend Layers

```text
Presentation Layer
        │
        ▼
API Layer (Views / Serializers)
        │
        ▼
Application Services
        │
        ▼
Domain Logic
        │
        ▼
Infrastructure Layer
        │
        ▼
Database / External Services
```

Business rules must never reside in API views.

---

# 5. Project Structure

```text
backend/

├── config/
│   ├── settings/
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│
│   ├── authentication/
│   ├── users/
│   ├── projects/
│   ├── datasets/
│   ├── generation/
│   ├── privacy/
│   ├── validation/
│   ├── exports/
│   ├── audit/
│   ├── common/
│   └── notifications/
│
├── services/
│
├── core/
│
├── utils/
│
├── media/
│
├── logs/
│
└── requirements/
```

---

# 6. Django Apps

## Authentication

Responsibilities:

* Registration
* Login
* JWT
* Password management
* Email verification

---

## Users

Responsibilities:

* User profile
* Preferences
* Account settings

---

## Projects

Responsibilities:

* Project lifecycle
* Ownership
* Dashboard

---

## Datasets

Responsibilities:

* Dataset
* DatasetField
* Schema
* Constraints

---

## Generation

Responsibilities:

* Generation Jobs
* AI orchestration
* Generator execution

---

## Privacy

Responsibilities:

* Privacy policy
* Privacy validation
* Differential privacy integration
* Privacy metadata

---

## Validation

Responsibilities:

* Structural validation
* Statistical validation
* Privacy validation coordination

---

## Exports

Responsibilities:

* CSV
* JSON
* XLSX
* Download management

---

## Audit

Responsibilities:

* Audit logs
* Activity history
* Security events

---

## Common

Shared utilities including:

* Base models
* Exceptions
* Pagination
* Constants
* Validators

---

# 7. API Layer

Responsibilities:

* Request validation
* Authentication
* Serialization
* Response formatting

API Views should:

* Be thin.
* Contain minimal business logic.
* Delegate work to services.

---

# 8. Service Layer

The Service Layer contains business workflows.

Examples:

* ProjectService
* DatasetService
* GenerationService
* PrivacyService
* ExportService
* ValidationService

Services:

* Coordinate multiple models.
* Execute business rules.
* Manage transactions.
* Return structured results.

Views communicate with services—not directly with unrelated business logic.

---

# 9. Domain Layer

The domain layer contains the business concepts and rules for:

* Projects
* Datasets
* Dataset Fields
* Generation Jobs
* Export Jobs
* Validation Results

Domain rules should remain independent of HTTP concerns wherever practical.

---

# 10. Data Access

The backend primarily uses Django's ORM.

Complex database operations should be encapsulated in dedicated query methods or managers rather than scattered throughout the codebase.

Avoid embedding large database queries directly in API views.

---

# 11. Background Jobs

Long-running operations should execute asynchronously.

Examples:

* Large dataset generation
* Validation
* Export packaging
* Email notifications

The architecture should support migration to Celery without changing business logic.

---

# 12. Error Handling

Errors should be:

* Structured
* Consistent
* Logged
* Traceable

Business exceptions should be separated from framework exceptions.

API responses should expose user-friendly messages while avoiding disclosure of sensitive implementation details.

---

# 13. Security

The backend shall implement:

* JWT authentication
* Role-based authorization
* Input validation
* Secure password storage
* CSRF protection where applicable
* Rate limiting
* Secure configuration management

---

# 14. Dependency Rules

Allowed dependency direction:

```text
Views
   ↓
Services
   ↓
Domain
   ↓
Infrastructure
```

Forbidden:

* Views calling unrelated apps directly.
* Models containing presentation logic.
* Serializers implementing business workflows.
* Circular dependencies between apps.

---

# 15. Logging

The backend shall log:

* Authentication events
* Generation jobs
* Privacy events
* Validation failures
* Export operations
* Critical exceptions

Logging should support future centralized observability platforms.

---

# 16. Testing Strategy

Backend testing should include:

* Unit Tests
* Integration Tests
* API Tests
* Permission Tests
* Validation Tests
* Privacy Workflow Tests

Testing architecture is detailed in `13_TESTING_STRATEGY.md`.

---

# 17. Extensibility

The backend should support:

* Additional AI generators
* Plugin-based validators
* New export formats
* Enterprise integrations
* Object storage providers
* Background processing engines

without requiring significant architectural changes.

---

# 18. Related Documents

* 03_SYSTEM_ARCHITECTURE.md
* 04_AI_ARCHITECTURE.md
* 05_PRIVACY_ARCHITECTURE.md
* 06_DATA_GENERATION_PIPELINE.md
* 08_DATABASE_DESIGN.md
* 09_API_SPECIFICATION.md
* 10_CODING_STANDARDS.md

---

# Version History

| Version | Date          | Description                                                                                     |
| ------- | ------------- | ----------------------------------------------------------------------------------------------- |
| 1.0.0   | Initial Draft | Backend architecture defining layers, modules, dependency rules, and implementation guidelines. |
