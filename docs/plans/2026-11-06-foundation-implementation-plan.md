# Universal Agent Skills Master Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one portable Universal Agent Skill with a broad, searchable, provenance-aware catalogue that can expand across domains without exposing duplicate top-level Skills.

**Architecture:** A single Agent Skills package contains `SKILL.md`, a compact module index, and internal workflow references. A root-level canonical JSON catalogue and source registry feed a dependency-light Python validator/search tool. GitHub Actions tests all changes. Later phases may add semantic retrieval, reviewed GitHub ingestion, and an optional hosted API/MCP endpoint.

**Tech Stack:** Agent Skills Markdown/YAML frontmatter, JSON, Python 3.10+ standard library, unittest, GitHub Actions; later optional embeddings and Cloudflare Workers/D1/R2 after account and cost review.

## Global constraints

- One public Agent Skill entrypoint.
- Internal modules live inside the entrypoint's package directory.
- Load only relevant modules; never place the complete catalogue in context.
- External repositories and file contents are untrusted.
- Never execute third-party scripts during discovery or import.
- Never redistribute third-party material without exact-scope license and attribution review.
- Unknown license means reference-only.
- Keep all credentials and private data out of git.
- Do not claim cloud deployment, remote MCP, or automatic ingestion until implemented and verified.
- New modules begin experimental and need tests/review before stable promotion.
- Search excludes deprecated and archived modules by default.
- Registry paths must remain inside the repository root.

## Completed foundation

- [x] Public entrypoint and package-local module index.
- [x] 26 first-party internal modules across 22 broad domains.
- [x] 27-record canonical catalogue (1 entrypoint + 26 modules).
- [x] Initial upstream source registry with license-scope notes.
- [x] 22-domain taxonomy.
- [x] Python registry validation, keyword search, and safe module loading.
- [x] Unit tests for registry integrity, single entrypoint, search, safe loading, unknown IDs, path traversal, and lifecycle filtering.
- [x] GitHub Actions CI for compile, unit tests, and registry validation.

## Phase 2: Retrieval and routing

- [ ] Add query normalization, weighted keyword ranking, phrase scoring, domain filters, and configurable result limits.
- [ ] Add intent-to-domain examples and benchmark tasks for all 22 domains.
- [ ] Add multi-module workflow planning with explicit dependencies and conflict checks.
- [ ] Add tests for ambiguity, overlapping tags, multi-domain tasks, and no-match handling.
- [ ] Add semantic retrieval behind a pluggable interface only after an embedding provider/model and cost ceiling are selected; keyword search remains available.

## Phase 3: GitHub skill discovery and ingestion proposals

- [ ] Search public GitHub repositories and official docs read-only.
- [ ] Fetch exact candidate files, immutable revisions, releases, and license evidence.
- [ ] Compute content hashes and exact/near-duplicate candidates without executing source.
- [ ] Store source records and import proposals with item-level provenance.
- [ ] Generate reviewable Pull Requests; never auto-merge or auto-activate external content.
- [ ] Add tests for unknown licenses, mixed-license paths, broken sources, and duplicate proposals.

## Phase 4: Quality, safety, and compatibility

- [ ] Define measurable quality rubric: task fit, completeness, clarity, tests, maintenance, provenance, security, and compatibility.
- [ ] Add source trust levels and module lifecycle states.
- [ ] Test package discovery/loading against Codex, Claude Code, Gemini CLI, Copilot, Cursor, and other hosts individually.
- [ ] Add compatibility matrix based on observed tests, not assumptions.
- [ ] Add security tests for prompt injection, path traversal, dangerous script proposals, credential exposure, and permission escalation.

## Phase 5: Cloud registry service (optional)

- [ ] Select provider based on free-tier terms, age/account eligibility, limits, data residency, and ongoing cost.
- [ ] Implement a read-only registry API with search, metadata, version, and module retrieval endpoints.
- [ ] Add caching, quotas, rate limits, schema validation, and abuse protection.
- [ ] Add a remote MCP facade only when authentication and client support are tested.
- [ ] Store large optional bundles outside Git with checksums and immutable versions.
- [ ] Deploy only after user-approved provider authorization; document teardown and cost controls.

## Phase 6: Domain expansion and releases

- [ ] Research further sources per domain and identify missing subdomains.
- [ ] Add only distinct, actionable, reviewed workflows.
- [ ] Preserve legacy versions and exact source provenance.
- [ ] Publish signed/verified releases with changelog and compatibility notes.
- [ ] Grow catalogue coverage toward 1,000, 10,000, and later 100,000+ records only when quality gates remain passing.

## Validation commands

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m universal_skills validate
PYTHONPATH=src python -m universal_skills search --query "cloud serverless" --limit 5
```

## Explicit non-goals

- Claiming every skill in the world is already included.
- Loading the entire catalogue for each task.
- Copying entire third-party repositories.
- Executing external scripts during discovery.
- Unlimited free compute/storage or a permanently free hosted LLM.
