# DevOps & Infrastructure

## Trigger
Use for CI/CD, containers, build pipelines, infrastructure-as-code, deployment, monitoring, and reliability.

## Workflow
1. Inspect workflows, runtimes, permissions, secrets, branch rules, and release process.
2. Keep CI permissions least-privilege and pin third-party actions to trusted versions.
3. Separate validation, build, security checks, packaging, deployment, and rollback.
4. Cache only reproducible dependencies; never include secrets in artifacts/logs.
5. Add tests, lint, build, dependency review, and secret scanning.
6. Use approvals for production environments.
7. Make migrations and deploys observable and reversible where feasible.
8. Test failures, retries, cancellation, concurrency, and rollback.
9. Document runner needs, quotas, artifacts, and operational ownership.

Do not deploy production or change repository permissions without authorization. Never suppress failing checks to appear green.
