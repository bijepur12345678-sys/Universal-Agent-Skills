# Cloud Registry Worker

This directory contains source code for a read-only REST API and stateless MCP server. It is source code only until an eligible account owner deploys and verifies it.

## Runtime behavior

- Reads the canonical registry and first-party module Markdown from this repository using an immutable Git commit SHA.
- Exposes read-only REST endpoints:
  - GET /health
  - GET /v1/domains
  - GET /v1/capabilities?query=...
  - GET /v1/modules/:module_id
  - GET /v1/workflows/:capability_id
  - GET /v1/sources/discover?query=...
- Exposes a stateless MCP endpoint at /mcp with four read-only tools:
  - search_capabilities
  - list_domains
  - get_skill_module
  - get_capability_workflow
  - discover_github_sources

## Safety and data boundaries

- The Worker has no shell, filesystem-write, deployment, account-management, GitHub-write, or arbitrary-code-execution tools.
- GitHub discovery returns repository metadata only. Every candidate remains review_required.
- A repository-level SPDX license is only a discovery signal; it does not prove that all paths or contributions are redistributable.
- The Worker never clones, installs, executes, copies, imports, publishes, or activates third-party Skills.
- Module retrieval is restricted to internal first-party module IDs and a fixed path prefix.
- The only upstream host used for module data is raw.githubusercontent.com; callers cannot supply a URL or arbitrary path.
- SOURCE_REF must be an immutable 40-character commit SHA. Do not use a moving branch or tag in production.
- Public REST and MCP responses contain public project material only. Do not add private user data or credentials to this service.
- MCP uses Cloudflare's SDK v2 stateless createMcpHandler; the deprecated stateful McpAgent API is not used.
- Origin validation uses the handler defaults. CORS is not authentication.
- Provider deployment is optional and must be performed only by an account owner eligible under the provider's current terms. No deployment, account mutation, or paid resource is performed by this repository change.

## Free-tier envelope

Cloudflare currently documents Workers Free at 100,000 requests/day and 10 ms CPU per request. These are provider limits, not a guarantee of uninterrupted service. Upstream GitHub search has separate rate limits; discovery errors are surfaced instead of silently inventing candidates.

## Configuration

Set SOURCE_REF in wrangler.jsonc to the reviewed immutable commit SHA that contains registry/capabilities.json, registry/domains.json, registry/catalog.json, and all first-party Markdown module files referenced by the catalogue.

No token is required to serve public registry data. Do not add GitHub or Cloudflare tokens to source files or vars.

## Development checks

Run npm install, npm run check, npm test, and npm run deploy:dry-run in the Cloud Worker directory. The deployment dry run bundles the Worker but does not publish it. A successful build is not evidence of a live deployment.
