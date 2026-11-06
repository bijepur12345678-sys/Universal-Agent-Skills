# Domain Module: Databases

## Trigger
Use for SQL, PostgreSQL, Supabase, NoSQL, schema design, migrations, indexing, query performance, backup, and data integrity.

## Workflow
1. Identify database engine/version, schema, data size, workload pattern, and environment.
2. Review existing schema and migrations before proposing changes.
3. Define primary keys, constraints, relationships, nullability, and lifecycle semantics.
4. Use parameterized queries and server-side authorization; never build SQL by concatenating untrusted input.
5. Plan migrations for existing data, locks, backfills, rollback, and compatibility with old application versions.
6. Add indexes based on measured query plans and expected write/read ratio.
7. Test constraints, transaction boundaries, concurrent updates, and authorization policies.
8. Define backup, point-in-time recovery, retention, and restore tests.
9. Review sensitive data minimization and access logging.

## Outputs
Schema/migration proposal, queries, performance evidence, integrity tests, and recovery notes.

## Boundaries
Never run destructive queries on production without explicit approval and verified backups. Do not expose private records in logs or examples.
