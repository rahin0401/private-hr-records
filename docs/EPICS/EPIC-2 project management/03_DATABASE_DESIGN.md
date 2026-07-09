# EPIC-02 — Project Workspace Management

## 03_DATABASE_DESIGN.md

---

# Document Information

| Property | Value |
|----------|-------|
| Project | Privacy-Preserving Synthetic HR Records Generator |
| Epic | EPIC-02 |
| Document | Database Design |
| Version | 1.0.0 |
| Status | Draft |
| Depends On | 00_EPIC_OVERVIEW.md, 01_FEATURE_BREAKDOWN.md, 02_USER_STORIES.md |

---

# 1. Purpose

This document defines the database architecture for **EPIC-02 – Project Workspace Management**.

It specifies the data model, entity relationships, constraints, indexes, lifecycle behavior, and future extensibility while maintaining consistency with the project's Clean Architecture principles.

The database design must support future epics without requiring schema redesign.

---

# 2. Design Principles

The Project database model shall follow:

- Third Normal Form (3NF)
- Data Integrity
- Referential Integrity
- Soft Delete Strategy
- Future Extensibility
- Audit Compatibility
- High Query Performance
- PostgreSQL Optimization

---

# 3. Core Entity

```
User

│

└── Project

      │

      ├── Dataset (EPIC-03)

      ├── DatasetField (EPIC-04)

      ├── Privacy Configuration (EPIC-05)

      ├── Generation Jobs (EPIC-06)

      ├── Generated Dataset (EPIC-06)

      ├── Export Jobs (EPIC-08)

      └── Activity Logs (Future)
```

The **Project** entity acts as the root business entity for every future resource.

---

# 4. Entity Overview

## Project

Represents an isolated workspace owned by a single authenticated user.

Every dataset, schema, generation job, privacy configuration, and generated dataset belongs to exactly one project.

---

# 5. Project Table

## Table Name

```
projects
```

---

## Columns

| Column | Type | Nullable | Description |
|----------|------|----------|-------------|
| id | UUID | No | Primary Key |
| owner_id | FK(User) | No | Project Owner |
| name | VARCHAR(150) | No | Project Name |
| slug | VARCHAR(180) | No | URL Friendly Identifier |
| description | TEXT | Yes | Project Description |
| status | VARCHAR(20) | No | Lifecycle Status |
| created_at | TIMESTAMP | No | Creation Time |
| updated_at | TIMESTAMP | No | Last Modification |
| archived_at | TIMESTAMP | Yes | Archive Timestamp |
| deleted_at | TIMESTAMP | Yes | Soft Delete Timestamp |
| created_by | FK(User) | No | Creator |
| updated_by | FK(User) | Yes | Last Modifier |

---

# 6. Primary Key

```
id (UUID)
```

UUIDs prevent predictable identifiers and improve security for public-facing APIs.

---

# 7. Foreign Keys

| Column | References |
|----------|------------|
| owner_id | User |
| created_by | User |
| updated_by | User |

---

# 8. Project Status

Allowed values:

```
ACTIVE

ARCHIVED

DELETED
```

Future versions may introduce:

- DRAFT
- READ_ONLY
- LOCKED

---

# 9. Entity Relationships

```
User

1

│

N

↓

Project
```

Future relationships:

```
Project

1

│

N

↓

Dataset
```

```
Project

1

│

N

↓

GenerationJob
```

```
Project

1

│

N

↓

GeneratedDataset
```

---

# 10. Constraints

## Primary Key

```
PRIMARY KEY (id)
```

---

## Foreign Key

```
owner_id

REFERENCES users(id)
```

---

## Unique Constraint

Project names must be unique for each owner.

```
UNIQUE(owner_id, name)
```

Different users may create projects with identical names.

---

## NOT NULL Constraints

Required fields:

- owner_id
- name
- slug
- status
- created_at

---

# 11. Soft Delete Strategy

Projects are never physically removed during normal operations.

Instead:

```
deleted_at

!= NULL
```

indicates the project has been deleted.

Benefits:

- Prevent orphaned records
- Preserve audit history
- Allow restoration
- Maintain referential integrity

---

# 12. Lifecycle Rules

```
ACTIVE

↓

ARCHIVED

↓

ACTIVE

↓

DELETED
```

Rules:

- Archived projects remain accessible.
- Deleted projects are hidden.
- Future restoration supported.

---

# 13. Index Strategy

Indexes should be created on:

```
owner_id

name

status

slug

created_at

updated_at

deleted_at
```

Composite index:

```
(owner_id, status)
```

Composite index:

```
(owner_id, name)
```

These optimize ownership queries and dashboard performance.

---

# 14. Slug Generation

Each project receives a unique slug.

Example

```
employee-data

synthetic-hr

banking-demo

payroll-system
```

Slug uniqueness is enforced per owner.

---

# 15. Audit Fields

Every project stores:

```
created_by

updated_by

created_at

updated_at
```

These fields simplify future audit reporting.

---

# 16. Data Integrity Rules

The database shall ensure:

- Owner exists
- Status valid
- Name unique per owner
- Soft delete consistency
- No orphaned references

---

# 17. Future Expansion

Future tables will reference Project.

```
Project

↓

Dataset

↓

DatasetField

↓

GenerationJob

↓

GeneratedDataset

↓

ExportJob
```

No future module shall bypass the Project entity.

---

# 18. Example Entity Diagram

```
+----------------------+
| User                 |
+----------------------+
| id                   |
| username             |
| email                |
+----------+-----------+
           |
           |
           | 1
           |
           | N
+----------v-----------+
| Project              |
+----------------------+
| id (UUID)            |
| owner_id             |
| name                 |
| slug                 |
| description          |
| status               |
| created_at           |
| updated_at           |
| archived_at          |
| deleted_at           |
| created_by           |
| updated_by           |
+----------------------+
```

---

# 19. Database Naming Standards

Tables

Plural

Examples:

```
projects

datasets

dataset_fields

generation_jobs
```

Columns

Snake case

Examples:

```
created_at

updated_at

owner_id

deleted_at
```

Foreign Keys

```
owner_id

project_id

dataset_id
```

---

# 20. Migration Strategy

Migration Order

```
User

↓

Project

↓

Dataset

↓

Dataset Field

↓

Generation

↓

Export
```

No future migration shall modify the ownership architecture established by Project.

---

# 21. Performance Considerations

The schema is designed to support:

- Millions of projects
- Efficient ownership filtering
- Fast dashboard statistics
- Pagination
- Soft delete filtering
- Future partitioning if required

---

# 22. Security Considerations

Database design shall enforce:

- Ownership isolation
- Foreign key integrity
- UUID identifiers
- Soft deletion
- No direct cross-user relationships

Authorization remains enforced at the application layer.

---

# 23. Definition of Done

Database design is complete when:

- Schema normalized
- Constraints defined
- Indexes documented
- Relationships complete
- Future compatibility verified
- Migration plan approved

---

# 24. Related Documents

- 00_EPIC_OVERVIEW.md
- 01_FEATURE_BREAKDOWN.md
- 02_USER_STORIES.md
- 04_BACKEND_IMPLEMENTATION.md
- 06_API_IMPLEMENTATION.md

---

# Version History

| Version | Description |
|----------|-------------|
| 1.0.0 | Initial database design for EPIC-02 Project Workspace Management |