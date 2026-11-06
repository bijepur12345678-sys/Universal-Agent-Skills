# Universal Agent Skills

**One public Agent Skill. 26 internal workflow modules. 176 granular task capabilities across 22 domains. One curated catalogue and intelligent routing model.**

Universal Agent Skills is an open-source, modular Agent Skill package. It exposes one installable entrypoint and keeps domain workflows inside that package, so compatible agents can discover one Skill rather than a confusing collection of unrelated top-level Skills.

> **Status: foundation release (0.1.0-dev).** The public Skill package, 26 internal modules, 22-domain taxonomy, initial source registry, 176 experimental capability workflow sections, deterministic routing/validation CLI, and GitHub Actions checks are present. The Cloudflare Worker and remote MCP implementation are source templates until deployed and tested. Semantic embeddings, automated GitHub ingestion, and comprehensive coverage are not yet complete.

## Core design

- **One public Skill:** `skills/universal-agent/SKILL.md`.
- **Internal modules:** `skills/universal-agent/references/modules/` contains 26 reusable domain and maintenance workflows.
- **Granular capabilities:** `registry/capabilities.json` contains 176 task-level workflow sections (eight per each of 22 domains), stored in `skills/universal-agent/references/capability-workflows.md`. Each section maps to an existing parent module; they are internal workflows, not separate public Skills.
- **Progressive loading:** search capability metadata first, deduplicate module IDs, then load only a few relevant workflows.
- **Canonical registry:** `registry/catalog.json` stores IDs, descriptions, domains, paths, versions, status, tags, licenses, and source references.
- **Provenance:** `registry/sources.json` records upstream projects and observed license scope.
- **Trust gates:** unknown license means reference-only; external scripts are never run during discovery.
- **Expandable:** new domains and modules can be added without creating more public entrypoints.

## Domains

AI/ML, Agentic AI, Software Engineering, Frontend, Backend, Cloud, DevOps, Databases, Research, UI/UX, Browser, Desktop, Mobile, Media, YouTube, Automation, Documents, Data Science, Security Analysis, Testing/QA, Education, and Business/Operations.

## Official upstream source coverage

The source registry includes 28 upstream repositories and official documentation references, including Microsoft, Cloudflare, Vercel, Supabase, GitHub, Anthropic, LangChain, Playwright, and the MCP ecosystem. The Microsoft review includes `microsoft/skills`, `microsoft/azure-skills`, `MicrosoftDocs/agent-skills`, `microsoft/agent-framework`, `microsoft/mcp`, and `microsoft/waza`. These are candidates/references—not blanket authorization to copy or execute them. Every individual Skill still needs task-fit, exact-path license, provenance, compatibility, security, and overlap review. See [the Microsoft ecosystem review](docs/research/microsoft-ecosystem-scan-2026-11-06.md) and [registry/sources.json](registry/sources.json).

## Repository map

| Path | Responsibility |
|---|---|
| `skills/universal-agent/SKILL.md` | Single public Agent Skill |
| `skills/universal-agent/references/module-index.md` | Compact package-local module discovery index |
| `skills/universal-agent/references/capability-workflows.md` | 176 individually retrievable task workflow sections |
| `skills/universal-agent/references/modules/` | 26 packaged internal workflows |
| `registry/catalog.json` | Canonical module catalogue |
| `registry/capabilities.json` | Granular capability records and routing metadata |
| `registry/sources.json` | Upstream source and license-scope records |
| `registry/domains.json` | 22-domain taxonomy |
| `src/universal_skills/` | Registry validator, keyword search, safe loader, capability router |
| `tests/` | Automated tests |
| `cloud/worker/` | Cloudflare REST API and stateless remote MCP Worker source |
| `docs/` | Architecture, source policy, and implementation roadmap |
| `.github/workflows/validate.yml` | Python and Worker validation |

## Local toolkit commands

The Skill Markdown package does not need local installation to read. The optional developer CLI requires Python 3.10+.

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m universal_skills validate
PYTHONPATH=src python -m universal_skills search --query "cloud serverless" --limit 5
PYTHONPATH=src python -m universal_skills route --task "build a Cloudflare Workers serverless API"
PYTHONPATH=src python -m universal_skills show-capability --id cloud-serverless-apps
PYTHONPATH=src python -m universal_skills capability-validate
```

Example router output includes the chosen capability, workflow reference, parent module ID, matched terms, required tools, missing tools, risk level, and approval flag. Load the selected workflow section by ID. Routing is deterministic and explainable; it is not an LLM semantic reranker.

## Cloud registry and MCP

A stateless Cloudflare Worker source template lives in `cloud/worker/`:

- Read-only REST endpoints: `/health`, `/v1/domains`, `/v1/capabilities`, and `/v1/modules/:id`.
- Read-only MCP tools: `search_capabilities`, `list_domains`, `get_skill_module`, `get_capability_workflow`, and `discover_github_sources`.
- No shell, write, deployment, GitHub mutation, or arbitrary code execution tools are exposed.
- The Worker serves bundled registry metadata. To return the exact module Markdown, set `SOURCE_REF` to an immutable Git commit SHA after a reviewed release is published.
- Cloud deployment is not claimed until a Cloudflare account, scoped permissions, deployment, and live endpoint tests are completed. No API key is stored in this repository.

See [Cloud Worker deployment notes](cloud/worker/README.md).

## Scale strategy

A long-term target is 100,000+ curated catalogue records, not 100,000 instructions in the model context. Keep metadata compact, rank candidates, deduplicate module IDs, and lazy-load only the selected workflows. Shard domain packages or move metadata to D1/another indexed store when measured size and latency require it. Large binaries and model weights belong in versioned external storage with checksums, not Git history.

## Roadmap

- [x] One public Skill package with 26 internal modules across 22 domains.
- [x] Source provenance and license review policy.
- [x] Registry validation, keyword search, safe loading, unit tests, and CI.
- [x] 176 granular experimental capability workflows and deterministic task routing.
- [x] Read-only Cloudflare REST/MCP source template.
- [ ] GitHub Actions verification of the complete branch.
- [ ] Semantic embeddings, reranking, and routing benchmarks.
- [ ] Read-only GitHub discovery/import proposals with manual review.
- [ ] Host compatibility adapters, tested per platform.
- [ ] Cloudflare deployment and live API/MCP smoke tests.
- [ ] Expand reviewed skill coverage based on quality, source evidence, and user demand.

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [source policy](docs/source-policy.md), and [NOTICE.md](NOTICE.md) before contributing upstream-derived material.

## License

First-party project code and content are Apache-2.0. Third-party materials retain their own licenses and notices.
