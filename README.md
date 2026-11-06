# Universal Agent Skills

**One entrypoint. A curated, extensible capability catalogue. One intelligent route to the right workflow.**

Universal Agent Skills is an open-source project for AI agents to discover, select, and use task-specific instructions across many domains. It exposes **one public Agent Skills entrypoint** backed by internal modules, a machine-readable registry, source provenance, and validation tooling.

> **Status:** early foundation (v0.1.0-dev). The one-entrypoint package, initial taxonomy, source registry, and validation tooling are being built. A hosted runtime, remote MCP service, large-scale ingestion, and production semantic routing are roadmap items—not deployed features.

## Principles

- **One visible Skill:** `skills/universal-agent/SKILL.md` is the single public entrypoint. Domain modules are internal resources.
- **Progressive loading:** search metadata first; load only the few relevant modules.
- **Evidence before import:** external repositories are candidates, not trusted instructions or automatically reusable code.
- **Provenance by default:** record source URL, immutable revision, license scope, author attribution, and review status.
- **Safe updates:** new material enters review; it is never silently activated.
- **Portable:** follow the Agent Skills format and keep core tooling dependency-light.

## Repository map

| Path | Responsibility |
|---|---|
| `skills/universal-agent/SKILL.md` | Single public Agent Skills entrypoint |
| `skills/modules/` | Internal instructions loaded only when relevant |
| `registry/catalog.json` | Canonical module catalogue |
| `registry/sources.json` | Reviewed upstream source registry |
| `registry/domains.json` | Stable domain taxonomy |
| `src/universal_skills/` | Registry validation, search, and safe loading |
| `tests/` | Automated tests |
| `docs/` | Architecture and governance |

## Initial internal modules

- GitHub source research and repository evaluation.
- Skill authoring and quality criteria.
- License and provenance review.
- Registry maintenance, versioning, and duplicate handling.

These are first-party starter modules, not a claim that every domain is fully implemented.

## Validation

Requires Python 3.10+ for the optional local CLI. The Skill Markdown itself can be read without installing anything.

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m universal_skills validate
PYTHONPATH=src python -m universal_skills search --query "GitHub research" --limit 5
```

## Scale and roadmap

A long-term capacity target is 100,000+ catalogue records. This is not the current count and does not mean 100,000 instructions should be loaded into context. Large packages may be sharded by domain, while a single logical registry and one public entrypoint remain.

- [x] Define the one-entrypoint architecture and initial domain taxonomy.
- [x] Record source URLs and observed license scope.
- [ ] Implement semantic retrieval and routing benchmarks.
- [ ] Build a reviewed GitHub ingestion proposal workflow.
- [ ] Add agent compatibility adapters.
- [ ] Deploy an optional hosted registry API and remote MCP service.
- [ ] Expand domain coverage through quality and licensing gates.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [source policy](docs/source-policy.md), and [SECURITY.md](SECURITY.md) before proposing imported content.

## License

First-party code and content are Apache-2.0. Third-party resources remain under their own terms; see [NOTICE.md](NOTICE.md) and `registry/sources.json`.
