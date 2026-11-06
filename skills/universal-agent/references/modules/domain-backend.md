# Backend Development

## Trigger
Use for APIs, services, server-side logic, authentication, authorization, background jobs, and integrations.

## Workflow
1. Inspect runtime, routes, data model, auth, deployment target, and error conventions.
2. Define request/response contracts, validation, status codes, pagination, and versioning.
3. Enforce authentication and resource authorization server-side.
4. Validate untrusted input and encode output.
5. Use transactions and idempotency for retryable writes.
6. Add timeouts, bounded retries, rate limits, structured logs, and health checks.
7. Keep secrets in an approved secret manager, never source code.
8. Test permissions, failure paths, integration behavior, and migrations.
9. Document API contracts, operational dependencies, and rollback.

Do not trust client-supplied ownership/roles or expose stack traces and internal records.
