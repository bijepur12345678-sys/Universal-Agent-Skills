# Domain Module: DevOps & Infrastructure

## Trigger
Use for CI/CD, containerization, build pipelines, release automation, infrastructure-as-code, monitoring, or reliability engineering.

## Workflow
1. Inspect current workflow files, runtimes, secrets usage, branch protections, and release process.
2. Keep CI permissions least-privilege and pin third-party actions to trusted versions or immutable references where appropriate.
3. Separate validation, build, security scan, packaging, deploy, and rollback stages.
4. Cache only reproducible dependencies and avoid storing secrets in artifacts or logs.
5. Add lint, tests, build, dependency review, secret checks, and artifact integrity verification.
6. Use environment approvals for production deployments.
7. Make migrations and deploys observable and reversible where possible.
8. Test failed jobs, retries, cancellation, concurrency, and rollback.
9. Document runner requirements, quotas, artifacts, and operational ownership.

## Outputs
Reproducible pipeline changes, release procedure, observability plan, and verified job results.

## Boundaries
Do not deploy to production or change repository permissions without explicit authorization. Do not suppress failing checks to make CI green.
