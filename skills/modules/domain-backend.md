# Domain Module: Backend Development

## Trigger
Use for API design, server-side application logic, authentication, authorization, background jobs, integrations, and service reliability.

## Workflow
1. Inspect the current runtime, routes, data model, authentication, deployment target, and error conventions.
2. Define request/response contracts, validation, status codes, pagination, and versioning.
3. Enforce authentication and authorization server-side for every protected resource.
4. Validate all untrusted input and encode output appropriately.
5. Use transactions and idempotency keys for operations that may be retried.
6. Add timeouts, bounded retries, rate limits, structured logs, and health checks.
7. Keep secrets in an approved secret manager/environment, never in source code.
8. Add unit, integration, permission-boundary, and failure-path tests.
9. Document API contracts, migrations, operational dependencies, and rollback behavior.

## Outputs
A typed service/API design or implementation with tests, observability, and operational notes.

## Boundaries
Do not trust client-supplied ownership or role claims. Do not expose stack traces, secrets, or internal data to callers.
