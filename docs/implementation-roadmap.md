# Implementation Roadmap

## Product contract

- One public Agent Skill entrypoint: `skills/universal-agent/SKILL.md`.
- Internal modules and capability records are not separate top-level Skills.
- The registry is a curated metadata catalogue, not a promise that every imaginable task already has a tested implementation.
- The long-term 100,000+ target means searchable records and reviewed source references, not 100,000 instructions loaded into model context.
- Third-party source code and instructions are never bulk-copied. Every candidate is reviewed at file/path scope for license, attribution, safety, maintenance, compatibility, and overlap.
- Discovery is read-only. Imported material is never executed or automatically activated.

## Current baseline (verified from repository)

- One public Skill entrypoint.
- 26 internal workflow modules across 22 domains.
- Curated upstream source registry and Microsoft ecosystem scan.
- Python registry validation, keyword search, safe module loading, tests, and GitHub Actions validation.
- No hosted API, deployed MCP endpoint, automatic source ingestion, or semantic embedding service yet.

## Delivery phases

### Phase A — Capability-level routing
- Add a granular capability registry with multiple task-level records per domain.
- Map each capability to an existing internal workflow module.
- Add deterministic and explainable ranking, tool prerequisites, risk level, and approval flags.
- Add validator and CLI commands.
- Keep all first-release records experimental until benchmarked.

### Phase B — Cloud registry source
- Add a Cloudflare Worker using the current stateless Agents SDK MCP handler.
- Expose read-only REST and MCP tools: search capabilities, retrieve a Skill module, and list domains.
- Use the public GitHub repository as the content source; pin the deployed source to an immutable release/commit.
- Support D1 as an optional metadata index for larger catalogues, with a static JSON fallback for development.
- Never expose write, deployment, or account mutation tools through the public registry endpoint.

### Phase C — Repository discovery and review queue
- Query public GitHub repository metadata and trees using read-only API calls.
- Detect Agent Skill candidates and collect source URL, immutable revision, paths, license evidence, release and maintenance signals.
- Create reviewable candidate records only. Do not copy candidate contents, execute scripts, or auto-activate sources.
- Require exact-path license and security review before first-party adaptation or redistribution.

### Phase D — Quality and compatibility
- Add routing benchmark cases for every domain.
- Add duplicate/near-duplicate reports and stable-ID checks.
- Validate Agent Skills format and test compatibility adapters only on platforms actually exercised.
- Preserve legacy resources with replacement links and lifecycle status.

### Phase E — Scale and release
- Expand reviewed capabilities by user demand and evidence.
- Use domain shards and D1/other indexed storage when GitHub file count, payload size, or search latency warrants it.
- Publish versioned releases, changelog, source notices, and contributor process.
- Keep cloud deployment separate from source-code readiness; deployment requires a configured provider account and scoped secrets.

## Cloud security boundaries

- Search and retrieval endpoints are read-only.
- No public arbitrary code execution, shell, filesystem write, GitHub write, deployment, or account-management tools.
- MCP uses Cloudflare's stateless `createMcpHandler` path and follows the provider's origin-validation defaults.
- Production deployment should use OAuth if any future tools access user-specific/private data.
- API keys and provider tokens belong only in encrypted platform secrets, never in Git history.

## Completion evidence

A phase is complete only when its tests run in GitHub Actions and the resulting run is inspected. A checked-in workflow or configuration file alone is not evidence of a successful deployment.
