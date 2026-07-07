# 09_API_SPECIFICATION.md

**Project:** Privacy-Preserving Synthetic HR Records Generator
**Document:** API Specification
**Version:** 1.0.0
**Status:** Draft
**Depends On:** 03_SYSTEM_ARCHITECTURE.md, 07_BACKEND_ARCHITECTURE.md, 08_DATABASE_DESIGN.md

---

# 1. Purpose

This document defines the REST API specification for the Privacy-Preserving Synthetic HR Records Generator.

It establishes endpoint conventions, request and response formats, authentication mechanisms, error handling, versioning, and resource design principles.

---

# 2. API Design Principles

The API shall:

* Follow REST principles.
* Use resource-oriented URLs.
* Return consistent response structures.
* Be versioned.
* Be stateless.
* Support pagination.
* Support filtering and ordering where applicable.
* Use appropriate HTTP status codes.
* Remain backward compatible whenever practical.

---

# 3. Base URL

Development:

```
/api/v1/
```

Future versions:

```
/api/v2/
```

Breaking changes require a new API version.

---

# 4. Authentication

Authentication Mechanism:

* JWT Access Token
* JWT Refresh Token

Authenticated requests shall include:

```
Authorization: Bearer <access_token>
```

Protected endpoints require a valid access token.

---

# 5. Standard Response Format

## Success

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {},
  "meta": {}
}
```

## Error

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {},
  "error_code": "VALIDATION_ERROR"
}
```

---

# 6. HTTP Status Codes

| Status | Meaning                     |
| ------ | --------------------------- |
| 200    | Success                     |
| 201    | Resource Created            |
| 202    | Accepted (Async Processing) |
| 204    | No Content                  |
| 400    | Bad Request                 |
| 401    | Unauthorized                |
| 403    | Forbidden                   |
| 404    | Not Found                   |
| 409    | Conflict                    |
| 422    | Validation Error            |
| 429    | Too Many Requests           |
| 500    | Internal Server Error       |

---

# 7. Authentication Endpoints

## Register

```
POST /auth/register/
```

Creates a new user account.

---

## Login

```
POST /auth/login/
```

Authenticates a user.

---

## Refresh Token

```
POST /auth/token/refresh/
```

Issues a new access token.

---

## Logout

```
POST /auth/logout/
```

Invalidates the current session.

---

## Profile

```
GET /auth/profile/
```

Returns the authenticated user's profile.

---

# 8. Project Endpoints

```
GET    /projects/
POST   /projects/
GET    /projects/{id}/
PUT    /projects/{id}/
PATCH  /projects/{id}/
DELETE /projects/{id}/
```

Supports:

* Pagination
* Search
* Ordering
* Ownership filtering

---

# 9. Dataset Endpoints

```
GET    /datasets/
POST   /datasets/
GET    /datasets/{id}/
PUT    /datasets/{id}/
PATCH  /datasets/{id}/
DELETE /datasets/{id}/
```

---

# 10. Dataset Field Endpoints

```
GET    /dataset-fields/
POST   /dataset-fields/
GET    /dataset-fields/{id}/
PUT    /dataset-fields/{id}/
PATCH  /dataset-fields/{id}/
DELETE /dataset-fields/{id}/
```

---

# 11. Generation Endpoints

## Start Generation

```
POST /generation/jobs/
```

Creates a new generation job.

---

## List Jobs

```
GET /generation/jobs/
```

---

## Job Details

```
GET /generation/jobs/{id}/
```

---

## Cancel Job (Future)

```
POST /generation/jobs/{id}/cancel/
```

---

# 12. Validation Endpoints

## Validation Result

```
GET /validation/{generation_job_id}/
```

Returns validation summaries for a generation job.

---

# 13. Export Endpoints

## Export Dataset

```
POST /exports/
```

Creates an export request.

---

## Export Status

```
GET /exports/{id}/
```

---

## Download Export

```
GET /exports/{id}/download/
```

Returns the generated export file when available.

---

# 14. Audit Endpoints

Administrative endpoints:

```
GET /audit/
GET /audit/{id}/
```

Access restricted to authorized roles.

---

# 15. Pagination

Collection endpoints should support:

```
?page=1
&page_size=20
```

Default page size should be configurable.

---

# 16. Filtering

Where appropriate, resources should support:

```
?status=completed
?created_after=...
?created_before=...
?owner=...
```

Filtering capabilities may differ by resource.

---

# 17. Ordering

Example:

```
?ordering=-created_at
```

Supported ordering fields should be documented for each resource.

---

# 18. Search

Resources may expose search functionality:

```
?search=employee
```

Search fields should be explicitly configured.

---

# 19. Validation Rules

Incoming requests shall be validated for:

* Required fields.
* Data types.
* Field lengths.
* Allowed values.
* Business constraints.
* Authorization.

Validation failures should return structured error responses.

---

# 20. Idempotency

The API should ensure that:

* GET requests are read-only.
* PUT replaces a resource.
* PATCH partially updates a resource.
* DELETE operations are safe to repeat where possible.

Future asynchronous operations may support idempotency keys.

---

# 21. Rate Limiting

Protected endpoints should support configurable rate limits.

Generation endpoints may use stricter limits due to resource consumption.

---

# 22. API Documentation

The platform should expose interactive API documentation.

Preferred tools:

* OpenAPI 3.x
* Swagger UI
* ReDoc

The API documentation should be automatically generated from the codebase whenever practical.

---

# 23. Security

The API shall implement:

* JWT authentication.
* Authorization checks.
* Input validation.
* Rate limiting.
* Secure headers.
* HTTPS in production.
* Sensitive data protection.

---

# 24. Versioning

Breaking API changes require a new major API version.

Minor enhancements should remain backward compatible.

Deprecated endpoints should follow a documented deprecation policy.

---

# 25. Related Documents

* 03_SYSTEM_ARCHITECTURE.md
* 07_BACKEND_ARCHITECTURE.md
* 08_DATABASE_DESIGN.md
* 10_CODING_STANDARDS.md
* 11_SECURITY_GUIDELINES.md

---

# Version History

| Version | Date          | Description                                                                                             |
| ------- | ------------- | ------------------------------------------------------------------------------------------------------- |
| 1.0.0   | Initial Draft | Initial REST API specification defining resources, conventions, authentication, and response standards. |
