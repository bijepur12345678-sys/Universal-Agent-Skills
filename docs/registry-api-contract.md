# Registry API and MCP Contract

## REST

| Method | Path | Query / input | Result |
|---|---|---|---|
| GET | /health | none | service status |
| GET | /v1/domains | none | domain taxonomy |
| GET | /v1/capabilities | query, optional domain, limit | ranked capabilities |
| GET | /v1/modules/:id | stable internal module ID | first-party module content |
| GET | /v1/sources/discover | query, optional limit | metadata-only GitHub candidates |

All endpoints are read-only. Invalid input receives a 4xx response; upstream failures receive a 502 response.

## MCP

Endpoint: /mcp using Streamable HTTP and a stateless SDK v2 handler.

### search_capabilities

Input: query, optional domain, limit, available_tools, include_legacy.

Output: ranked capability records including the internal module ID, matched terms, required/missing tools, risk level, and approval flag.

### get_capability_workflow

Input: capability_id.

Output: one section from the internal capability workflow pack. Unknown, deprecated, and archived capability IDs are not returned by default.

### list_domains

Input: none.

Output: the 22-domain taxonomy.

### get_skill_module

Input: module_id.

Output: the matching first-party internal workflow Markdown. Arbitrary paths and third-party source files are not accepted.

### discover_github_sources

Input: query, optional limit.

Output: public GitHub repository metadata, maintenance signals, repository-level license signal, caveats, and review_required state. It does not modify the registry.

## Routing semantics

The initial Worker uses deterministic phrase and token matching over trigger phrases, synonyms, names, and descriptions. It is explainable and dependency-free. It is not an embedding model or LLM reranker. Semantic retrieval can be added later behind the same contract after benchmark evidence.

## Versioning

The response schema is versioned by the /v1/ path. The Worker reads content from a fixed Git commit SHA supplied by SOURCE_REF. Update the pinned SHA only after a reviewed repository revision is available.
