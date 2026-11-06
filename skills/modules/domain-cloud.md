# Domain Module: Cloud Platforms

## Trigger
Use for cloud architecture, serverless applications, Workers, hosted agents, cloud storage, networking, and managed services.

## Workflow
1. Confirm provider, region, free-tier eligibility, data residency, account permissions, and budget ceiling.
2. Separate control plane, runtime, storage, secrets, queues, and observability.
3. Prefer managed/serverless resources for low-operations workloads when limits fit.
4. Define least-privilege identities, network boundaries, encryption, backups, and retention.
5. Estimate compute, storage, bandwidth, egress, logs, and request costs before deployment.
6. Use infrastructure-as-code or reproducible configuration where practical.
7. Add health checks, rate limits, quotas, retries, and failure isolation.
8. Test deploy, update, rollback, data restore, and permission boundaries in a non-production environment.
9. Record quotas, provider-specific limits, and a teardown procedure.

## Outputs
Provider-appropriate cloud architecture, cost model, configuration, deployment plan, and verification checklist.

## Boundaries
Never claim a service is deployed without a deployment result. Never create paid resources or bind billing without explicit user authorization.
