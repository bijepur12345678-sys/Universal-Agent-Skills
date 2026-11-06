# Universal Agent Skills Foundation Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a secure, portable one-entrypoint Agent Skills repository with a validated, searchable catalogue and evidence-backed source registry.

**Architecture:** One public `SKILL.md` entrypoint delegates to internal Markdown modules using a machine-readable JSON catalogue. A standard-library Python package validates and searches the catalogue; GitHub Actions runs checks on proposed changes.

**Tech Stack:** Agent Skills Markdown/YAML frontmatter, JSON, Python 3.10+ standard library, unittest, GitHub Actions.

## Global constraints

- One public installable entrypoint; internal modules are reference files, not separate auto-discovered Skills.
- Do not load the full catalogue into model context.
- External repositories and their contents are untrusted.
- Do not execute third-party scripts during discovery or validation.
- Do not redistribute material without exact-scope license and attribution review.
- Keep credentials and private data out of the repository.
- Do not claim a remote runtime or MCP endpoint is deployed until tested.
- Search excludes deprecated and archived modules by default.
- All catalogue paths remain inside the repository root.

## Deliverables

1. Governance, 22-domain taxonomy, source registry, and license policy.
2. One public entrypoint plus four internal first-party modules.
3. Registry validation, keyword search, safe module loading, and tests.
4. GitHub Actions validation on push, pull request, and manual dispatch.

## Validation commands

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m universal_skills validate
PYTHONPATH=src python -m universal_skills search --query "GitHub research" --limit 5
```

## Later independent plans

- Semantic retrieval and routing benchmarks.
- Read-only GitHub ingestion with reviewable proposals.
- Hosted registry API and remote MCP endpoint, after provider/cost/security selection.
- Domain skill expansion through quality and license gates.
- Compatibility adapters tested against each declared host.

## Decisions for later phases

- Which provider should host a remote API/MCP endpoint and what cost ceiling applies?
- Which agent hosts should be declared supported after end-to-end tests?
- Which embedding model and hosting budget are acceptable?
- When should domain packs be sharded into separate repositories?
