# Universal Agent Skills

**One public Agent Skill. 26 internal workflow modules. One curated catalogue and intelligent routing model.**

Universal Agent Skills is an open-source, modular Agent Skill package. It exposes one installable entrypoint and keeps domain workflows inside that package, so compatible agents can discover one Skill rather than a confusing collection of unrelated top-level Skills.

> **Status: foundation release (0.1.0-dev).** The public Skill package, 26 internal modules, 22-domain taxonomy, initial source registry, Python validation/search CLI, and CI checks are present. Hosted search, remote MCP, semantic ranking, automatic GitHub ingestion, and comprehensive coverage are not yet deployed.

## Core design

- **One public Skill:** `skills/universal-agent/SKILL.md`.
- **Internal modules:** `skills/universal-agent/references/modules/` contains 26 focused workflow modules.
- **Progressive loading:** read the module index, then load only a few relevant workflows.
- **Canonical registry:** `registry/catalog.json` stores IDs, descriptions, domains, paths, versions, status, tags, licenses, and source references.
- **Provenance:** `registry/sources.json` records upstream projects and observed license scope.
- **Trust gates:** unknown license means reference-only; external scripts are never run during discovery.
- **Expandable:** new domains and modules can be added without creating more public entrypoints.

## Domains

AI/ML, Agentic AI, Software Engineering, Frontend, Backend, Cloud, DevOps, Databases, Research, UI/UX, Browser, Desktop, Mobile, Media, YouTube, Automation, Documents, Data Science, Security Analysis, Testing/QA, Education, and Business/Operations.

## Repository map

| Path | Responsibility |
|---|---|
| `skills/universal-agent/SKILL.md` | Single public Agent Skill |
| `skills/universal-agent/references/module-index.md` | Internal module discovery index |
| `skills/universal-agent/references/modules/` | 26 packaged internal workflows |
| `registry/catalog.json` | Canonical 27-entry catalogue (1 entrypoint + 26 modules) |
| `registry/sources.json` | Upstream source and license-scope records |
| `registry/domains.json` | 22-domain taxonomy |
| `src/universal_skills/` | Registry validator, search, and safe module loader |
| `tests/` | Automated tests |
| `docs/` | Architecture, import policy, and implementation plan |
| `.github/workflows/validate.yml` | GitHub Actions validation |

## Validation

The Skill Markdown package does not need local installation to read. The optional registry CLI requires Python 3.10+.

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m universal_skills validate
PYTHONPATH=src python -m universal_skills search --query "cloud serverless" --limit 5
```

## Scale strategy

A long-term target is 100,000+ catalogue records, not 100,000 instructions in the model context. Metadata stays compact, instructions load lazily, and domain packages may be sharded when repository/API limits require it. Large binaries and model weights belong in versioned external storage with checksums, not Git history.

## Roadmap

- [x] One public Skill package with 26 internal modules across 22 domains.
- [x] Source provenance and license review policy.
- [x] Registry validation, keyword search, safe loading, unit tests, and CI.
- [ ] Semantic retrieval, reranking, and routing benchmarks.
- [ ] Read-only GitHub discovery/import proposals with manual review.
- [ ] Host compatibility adapters, tested per platform.
- [ ] Hosted registry API and optional remote MCP endpoint.
- [ ] Expand reviewed skill coverage based on quality and user demand.

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [source policy](docs/source-policy.md), and [NOTICE.md](NOTICE.md) before contributing upstream-derived material.

## License

First-party project code and content are Apache-2.0. Third-party materials retain their own licenses and notices.
