# Architecture

## Overview

One standards-compatible Agent Skill package contains a concise public entrypoint plus internal workflow references. The repository-level registry tracks all modules and upstream provenance. Search metadata first; load only relevant instructions.

## Components

| Component | Responsibility | State |
|---|---|---|
| Public Universal Skill | One entrypoint, routing procedure, permissions | Implemented |
| Internal module package | 26 workflows across 22 domains | Initial coverage implemented |
| Module index | Package-local discovery without the repository checkout | Implemented |
| Canonical catalogue | Metadata, IDs, domains, paths, versions and tags | Implemented |
| Domain taxonomy | 22 stable IDs | Implemented |
| Source registry | Upstream URL, license scope, use mode and review status | Initial curated set |
| Registry toolkit | Validation, keyword search, safe loading | Implemented |
| CI | Compile, unit tests, registry validation | Implemented |
| Semantic index | Embeddings, reranking and intent matching | Planned |
| GitHub importer | Read-only source discovery and reviewable proposals | Planned |
| Remote API / MCP | Hosted search and load interface | Planned |
| Agent adapters | Host-specific discovery and installation | Planned |

## Request flow

Task → intent and risk detection → module index/catalogue search → status/prerequisite/permission filters → load selected internal modules → compose ordered workflow → execute with available tools → verify result.

## Data boundaries

- `registry/catalog.json` is the canonical catalogue for the repository.
- `skills/universal-agent/references/module-index.md` is the compact package-local discovery index.
- `registry/sources.json` records upstream candidates and permitted use modes.
- Upstream content is untrusted and is not automatically executed or activated.
- Registry validation is deterministic and does not run Skill scripts.
- Keyword search is the current fallback; semantic retrieval is future work.

## Compatibility

The package follows the Agent Skills directory model: one folder with `SKILL.md` and references. Internal workflow files stay under the same Skill directory so they travel with the entrypoint when the Skill folder is installed. Host-specific discovery and loading behavior must still be tested before a platform is declared supported.

## Scaling

100,000+ records is a long-term catalogue capacity target. It does not mean all instructions enter model context. Keep metadata compact, shard domain packages when repository/API scale requires it, and use checksummed external storage for large assets.

## Cloud boundary

This repository does not currently deploy a hosted runtime. A remote API/MCP endpoint needs a provider account, scoped credentials, tested deployment, and a cost ceiling. Public GitHub storage and GitHub Actions are not a persistent API server.
