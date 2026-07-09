# 03_DATABASE_DESIGN.md

**Project:** Privacy-Preserving Synthetic HR Records Generator
**Epic:** EPIC-01 – Authentication & User Management
**Document:** Database Design
**Version:** 1.0.0
**Status:** Draft

---

# 1. Purpose

This document defines the database design for the Authentication & User Management module.

It specifies the entities, relationships, constraints, indexes, and migration strategy required to implement authentication and user management.

---

# 2. Database Technology

* Database: PostgreSQL
* ORM: Django ORM
* Framework: Django 5.x + Django REST Framework

---

# 3. Database Entities

This epic contains the following entities:

| Entity      | Purpose                              |
| ----------- | ------------------------------------ |
| User        | Stores user account information      |
| UserSession | Tracks active user sessions/devices  |
| AuditLog    | Stores authentication-related events |

> **Note:** JWT blacklist tables are provided by `djangorestframework-simplejwt` when token blacklisting is enabled and should not be recreated.

---

# 4. Entity Relationship Diagram

```text
User
 │
 ├──────────────< UserSession
 │
 └──────────────< AuditLog
```

---

# 5. User Entity

### Description

Represents a platform user.

### Recommended Fields

| Field          | Type            | Constraints      |
| -------------- | --------------- | ---------------- |
| id             | UUID            | Primary Key      |
| username       | String          | Unique, Indexed  |
| email          | Email           | Unique, Indexed  |
| first_name     | String          | Nullable         |
| last_name      | String          | Nullable         |
| password       | Hashed Password | Required         |
| role           | Enum            | Default: USER    |
| status         | Enum            | Default: PENDING |
| is_active      | Boolean         | Default: False   |
| is_staff       | Boolean         | Default: False   |
| is_superuser   | Boolean         | Default: False   |
| email_verified | Boolean         | Default: False   |
| last_login     | DateTime        | Nullable         |
| created_at     | DateTime        | Auto Generated   |
| updated_at     | DateTime        | Auto Generated   |

### Status Enum

```text
PENDING
ACTIVE
SUSPENDED
DEACTIVATED
```

### Role Enum

```text
USER
ADMIN
```

---

# 6. UserSession Entity

### Description

Stores active login sessions.

### Fields

| Field            | Type             |
| ---------------- | ---------------- |
| id               | UUID             |
| user             | ForeignKey(User) |
| refresh_token_id | UUID/String      |
| device_name      | String           |
| device_type      | String           |
| ip_address       | String           |
| user_agent       | Text             |
| last_activity    | DateTime         |
| expires_at       | DateTime         |
| created_at       | DateTime         |

### Purpose

Supports:

* Active sessions
* Logout specific device
* Logout all devices
* Session history

---

# 7. AuditLog Entity

### Description

Stores security-related events.

### Fields

| Field       | Type                       |
| ----------- | -------------------------- |
| id          | UUID                       |
| user        | ForeignKey(User, Nullable) |
| event_type  | Enum                       |
| ip_address  | String                     |
| user_agent  | Text                       |
| description | Text                       |
| created_at  | DateTime                   |

### Event Types

* REGISTER
* LOGIN
* LOGIN_FAILED
* LOGOUT
* PASSWORD_CHANGED
* PASSWORD_RESET
* PROFILE_UPDATED
* EMAIL_VERIFIED
* ACCOUNT_LOCKED

---

# 8. Relationships

| Parent | Child       | Relation    |
| ------ | ----------- | ----------- |
| User   | UserSession | One-to-Many |
| User   | AuditLog    | One-to-Many |

---

# 9. Constraints

## User

* Username unique
* Email unique
* Password required
* Role required
* Status required

## UserSession

* Must belong to a User
* Expiration required

## AuditLog

* Event type required
* Timestamp required

---

# 10. Indexes

Create indexes for:

## User

* username
* email
* role
* status
* is_active

## UserSession

* user
* expires_at

## AuditLog

* user
* event_type
* created_at

---

# 11. Cascade Rules

| Parent             | Child    | Action |
| ------------------ | -------- | ------ |
| User → UserSession | CASCADE  |        |
| User → AuditLog    | SET NULL |        |

Reason:

* Sessions should be removed with the user.
* Audit logs should be preserved even if the user is removed.

---

# 12. Validation Rules

### Email

* Valid email format
* Unique

### Username

* 3–30 characters
* Unique
* Letters, numbers, underscore

### Password

* Django password validators
* Minimum length
* Common password check
* Numeric-only password rejection

---

# 13. Migration Order

1. Create Custom User Model
2. Apply Authentication Migrations
3. Create UserSession Model
4. Create AuditLog Model
5. Apply JWT Blacklist Migrations
6. Verify Constraints and Indexes

---

# 14. Data Lifecycle

### User

PENDING

↓

ACTIVE

↓

SUSPENDED (Optional)

↓

DEACTIVATED

---

### Session

CREATED

↓

ACTIVE

↓

EXPIRED / REVOKED

↓

DELETED

---

### Audit Log

Created

↓

Stored

↓

Archived (Future)

---

# 15. Performance Considerations

* UUID primary keys
* Indexed authentication fields
* Foreign key indexes
* Efficient session lookups
* Query optimization through ORM (`select_related` / `prefetch_related`) where appropriate

---

# 16. Security Considerations

* Never store plaintext passwords
* Store only hashed passwords
* Store minimal session information
* Avoid storing secrets in audit logs
* Record authentication activity for auditing

---

# 17. Future Expansion

The schema should support:

* Multi-Factor Authentication (MFA)
* OAuth Providers
* Single Sign-On (SSO)
* Organization membership
* Multi-tenancy
* Advanced roles and permissions
* User preferences
* Profile images

---

# 18. Definition of Done

Database implementation is complete when:

* All models created
* Relationships verified
* Migrations successful
* Constraints applied
* Indexes created
* Admin panel configured
* Unit tests passing

---

# 19. Related Documents

* 00_EPIC_OVERVIEW.md
* 01_FEATURE_BREAKDOWN.md
* 02_USER_STORIES.md
* 04_BACKEND_IMPLEMENTATION.md
* 06_API_IMPLEMENTATION.md

---

# Version History

| Version | Description                                                           |
| ------- | --------------------------------------------------------------------- |
| 1.0.0   | Initial database design for EPIC-01 Authentication & User Management. |
