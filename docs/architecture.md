# Architecture

## Overview

One Agent Skills entrypoint exposes a modular catalogue. Search metadata first; load selected module instructions only when relevant.

## Components

| Component | Responsibility | State |
|---|---|---|
| Universal Skill | Single public entrypoint and routing procedure | Foundation |
| Catalogue | Internal module metadata | Foundation |
| Domain taxonomy | Stable IDs and descriptions | Foundation |
| Source registry | Upstream URL, license scope and review status | Foundation |
| Registry toolkit | Validation, search and safe module loading | Next foundation increment |
| Semantic index | Embeddings and reranking | Planned |
| GitHub importer | Read-only discovery and reviewable proposals | Planned |
| Remote API / MCP | Hosted search and load interface | Planned |
| Agent adapters | Host-specific discovery/installation | Planned |

## Request flow

Task → intent and risk detection → catalogue search → status/prerequisite/permission filters → selected internal modules → ordered workflow → execution with available tools → verification.

## Data boundaries

- `catalog.json` is the canonical internal module list.
- `sources.json` records upstream candidates and permitted use mode.
- Upstream content is untrusted and not automatically executable.
- Registry validation is deterministic and does not execute skill scripts.
- Keyword search is the initial fallback; semantic retrieval is future work.

## Scaling

100,000+ records is a long-term catalogue capacity target. It does not mean all instructions enter context. Keep metadata compact, shard packages when needed, and use checksummed external storage for large assets.

## Cloud boundary

This repository does not currently deploy a cloud runtime. A remote API/MCP endpoint needs a provider account, scoped credentials, a tested deployment, and a cost ceiling. Public GitHub storage alone is not a server.
