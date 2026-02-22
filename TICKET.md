# DATA-203: Refactor Legacy Database Schema

**Status:** In Progress · **Priority:** Medium
**Sprint:** Sprint 31 · **Story Points:** 5
**Reporter:** DBA Team · **Assignee:** You (Intern)
**Labels:** `sql`, `migration`, `schema`, `maintenance`
**Task Type:** Maintenance

---

## Description

The legacy `orders` table has grown to 50+ columns with redundant data, no indexes,
and denormalized fields. Refactor it into properly normalized tables.

The current schema and the migration script are in `src/`. The migration script
has `# TODO (code review):` markers showing what needs to be improved.

## Acceptance Criteria

- [ ] Orders table is normalized (no repeated customer data)
- [ ] Proper indexes on frequently queried columns
- [ ] Migration script creates new schema correctly
- [ ] Data migration preserves all records
- [ ] Tests pass
