# 11_CODING_STANDARDS.md

**Project:** Privacy-Preserving Synthetic HR Records Generator
**Document:** Coding Standards
**Version:** 1.0.0
**Status:** Draft
**Depends On:** 00_PROJECT_CONSTITUTION.md, 07_BACKEND_ARCHITECTURE.md, 10_FRONTEND_ARCHITECTURE.md

---

# 1. Purpose

This document defines the coding standards for the Privacy-Preserving Synthetic HR Records Generator.

Its objective is to ensure that the codebase remains readable, maintainable, secure, testable, and consistent regardless of the number of contributors.

---

# 2. Engineering Principles

Every contributor shall follow:

* SOLID Principles
* DRY (Don't Repeat Yourself)
* KISS (Keep It Simple, Stupid)
* YAGNI (You Aren't Gonna Need It)
* Separation of Concerns
* Clean Architecture
* Composition over Inheritance where appropriate

When principles conflict, prioritize readability and maintainability.

---

# 3. General Rules

Code should:

* Be easy to read.
* Be easy to understand.
* Be easy to test.
* Be easy to modify.
* Avoid unnecessary complexity.
* Express intent clearly.
* Minimize hidden side effects.

---

# 4. Naming Conventions

## Variables

Use descriptive snake_case names.

Example:

```text
generation_job
privacy_score
dataset_schema
```

---

## Constants

Use UPPER_SNAKE_CASE.

Example:

```text
MAX_RECORD_COUNT
DEFAULT_PAGE_SIZE
JWT_EXPIRATION_MINUTES
```

---

## Classes

Use PascalCase.

Example:

```text
GenerationService
PrivacyValidator
DatasetSerializer
```

---

## Functions

Use descriptive snake_case names.

Functions should represent actions.

Examples:

```text
generate_dataset()
validate_schema()
export_dataset()
```

---

## Files

Python:

```text
generation_service.py
privacy_validator.py
```

React:

```text
GenerationPage.jsx
DatasetTable.jsx
```

---

# 5. Project Structure

Follow the folder organization defined in:

* 07_BACKEND_ARCHITECTURE.md
* 10_FRONTEND_ARCHITECTURE.md

Do not introduce new top-level folders without architectural review.

---

# 6. Function Design

Functions should:

* Perform one primary task.
* Have clear inputs and outputs.
* Minimize side effects.
* Remain reasonably small.
* Be reusable where appropriate.

Avoid "god functions" that perform multiple unrelated responsibilities.

---

# 7. Class Design

Classes should:

* Represent a single responsibility.
* Hide internal implementation details.
* Expose clear public interfaces.
* Avoid unnecessary inheritance.

Business logic should reside in services or domain objects rather than controllers or serializers.

---

# 8. API Views

API views shall:

* Handle HTTP concerns only.
* Delegate business logic to services.
* Validate requests.
* Return standardized responses.

Avoid embedding business workflows directly inside views.

---

# 9. Serializers

Serializers should:

* Validate incoming data.
* Transform representations.
* Avoid business logic.
* Remain focused on serialization concerns.

---

# 10. Models

Models should:

* Represent domain entities.
* Define relationships.
* Enforce simple integrity constraints.

Complex workflows should remain outside model methods unless tightly coupled to the entity.

---

# 11. Services

Services are responsible for:

* Business workflows.
* Cross-model operations.
* Transaction coordination.
* Orchestration.

Services should not contain presentation logic.

---

# 12. Error Handling

Errors should:

* Be explicit.
* Be meaningful.
* Preserve useful context for debugging.
* Avoid exposing sensitive implementation details.

Use custom exceptions for business-specific failures where appropriate.

---

# 13. Logging

Log:

* Authentication events.
* Generation jobs.
* Validation failures.
* Privacy events.
* Export operations.
* Unexpected exceptions.

Avoid logging sensitive information such as passwords, secrets, or raw confidential HR data.

---

# 14. Comments

Write comments to explain *why*, not *what*.

Prefer self-explanatory code over excessive comments.

Remove obsolete comments during refactoring.

---

# 15. Documentation

Public modules, services, and reusable components should include concise documentation describing:

* Purpose
* Inputs
* Outputs
* Expected behavior

Documentation should evolve alongside the code.

---

# 16. Code Reuse

Before introducing new code:

* Check for existing reusable implementations.
* Avoid duplication.
* Extract reusable logic when duplication becomes evident.

Do not create abstractions prematurely.

---

# 17. Security Practices

Contributors shall:

* Validate all external input.
* Avoid hardcoded secrets.
* Use environment variables for configuration.
* Follow the Security Guidelines document.
* Apply the principle of least privilege.

Security should be considered during implementation rather than after development.

---

# 18. Performance

Optimize based on measurement.

Prefer:

* Efficient database queries.
* Appropriate indexing.
* Pagination.
* Lazy evaluation where suitable.
* Bulk operations for large datasets.

Avoid premature optimization.

---

# 19. Testing Expectations

Code should be written with testing in mind.

Every significant feature should support:

* Unit testing.
* Integration testing.
* API testing where applicable.

Testing requirements are defined in `13_TESTING_STRATEGY.md`.

---

# 20. Git Standards

Recommended practices:

* Small, focused commits.
* Descriptive commit messages.
* Feature branches.
* Pull request reviews.
* No direct commits to protected production branches.

Commit messages should clearly describe the purpose of the change.

---

# 21. Code Review Checklist

Reviewers should verify:

* Correctness.
* Readability.
* Maintainability.
* Security.
* Performance considerations.
* Test coverage.
* Compliance with architecture documents.
* Compliance with this coding standard.

Code review is an engineering quality process, not merely a syntax check.

---

# 22. Prohibited Practices

Avoid:

* Business logic inside views.
* Business logic inside serializers.
* Circular dependencies.
* Large monolithic classes.
* Excessive nesting.
* Magic numbers.
* Hardcoded credentials.
* Duplicate code.
* Silent exception handling.
* Dead code.

Exceptions to these guidelines should be justified and documented.

---

# 23. Related Documents

* 00_PROJECT_CONSTITUTION.md
* 07_BACKEND_ARCHITECTURE.md
* 09_API_SPECIFICATION.md
* 10_FRONTEND_ARCHITECTURE.md
* 12_SECURITY_GUIDELINES.md
* 13_TESTING_STRATEGY.md

---

# Version History

| Version | Date          | Description                                                                                                                             |
| ------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | Initial Draft | Initial coding standards defining engineering principles, naming conventions, architectural responsibilities, and quality expectations. |
