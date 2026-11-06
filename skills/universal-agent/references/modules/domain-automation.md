# Automation & Integrations

## Trigger
Use for APIs, MCP, webhooks, scheduled jobs, cross-app workflows, and event-driven automation.

## Workflow
1. Define trigger, action, desired result, failure behavior, and owner.
2. Inventory existing connectors, auth scopes, quotas, and integrations before adding duplicates.
3. Prefer official APIs and narrow OAuth scopes; never hard-code tokens.
4. Validate inputs/responses and use idempotency for retryable writes.
5. Add timeouts, bounded retries, backoff, rate limits, and error reporting.
6. Separate read-only discovery from write-capable actions.
7. Require approval for destructive, public, financial, privacy-sensitive, or irreversible actions.
8. Log non-sensitive outcomes and correlation IDs only.
9. Test duplicate events, partial failure, expired auth, quotas, and rollback.

Never claim success until the connector confirms it. Do not silently broaden permissions.
