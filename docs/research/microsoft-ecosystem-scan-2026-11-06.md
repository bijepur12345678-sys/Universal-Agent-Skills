# Microsoft Agent Skills Ecosystem Review — 2026-11-06

## Purpose

This review adds official Microsoft repositories and documentation to the Universal Agent Skills source registry. These are **source candidates and references**, not blanket authorization to copy every file or install every tool.

## High-value sources

| Source ID | Upstream | Capability | Observed license and scope | Registry decision |
|---|---|---|---|---|
| `microsoft-skills` | https://github.com/microsoft/skills | Microsoft/Azure SDK and Foundry skills, custom agents, AGENTS.md templates, MCP configs | MIT repository license; inspect individual assets/contributions | Reviewed reference; candidate catalogue |
| `microsoftdocs-agent-skills` | https://github.com/MicrosoftDocs/agent-skills | Azure service guidance generated from Microsoft Learn; multi-host Agent Skills package | Skill/documentation content CC BY 4.0; code MIT | Reference-only pending exact-path attribution review |
| `microsoft-azure-skills` | https://github.com/microsoft/azure-skills | Azure workflows plus Azure MCP and Foundry MCP integration | MIT | Reviewed reference; tool actions still need Azure credentials/authorization |
| `microsoft-agent-framework` | https://github.com/microsoft/agent-framework | Python/.NET production agent and multi-agent orchestration framework | MIT | Reviewed reference; evaluate as primary Microsoft-aligned orchestration option |
| `microsoft-semantic-kernel` | https://github.com/microsoft/semantic-kernel | Existing Semantic Kernel projects and migration reference | MIT | Legacy compatibility reference; current README points new projects to Microsoft Agent Framework |
| `microsoft-mcp` | https://github.com/microsoft/mcp | Shared Microsoft MCP server libraries, test harnesses, pipelines, and tooling | MIT | Reviewed reference; inspect individual server packages, not the entire large repository |
| `microsoft-waza` | https://github.com/microsoft/waza | Evaluate agent workflows, Skills, custom agents, and MCP scenarios | MIT | Reviewed reference; verify tagged CLI version against current source behavior |
| `microsoft-win-dev-skills` | https://github.com/microsoft/win-dev-skills | Windows app development, WinUI, packaging, and debugging workflows | MIT | Reviewed reference; local OS/SDK prerequisites are optional and never auto-installed |
| `microsoft-power-platform-skills` | https://github.com/microsoft/power-platform-skills | Power Platform, Dataverse, Power Apps, Power Pages, and MCP Apps | MIT repository; inspect plugin-specific and third-party material | Reviewed reference |
| `microsoft-cat-agent-skills` | https://github.com/microsoft/cat-agent-skills | Searchable community gallery of Skills, plugins, and automations | MIT repository; preserve each contributor's original source/license notice | Reviewed reference; item-level review required |
| `microsoft-azure-devops-mcp` | https://github.com/microsoft/azure-devops-mcp | Azure DevOps MCP integration candidate | License not verified in this review | Review required; do not import or activate |

## Verified catalogue signals

- Microsoft `microsoft/skills` README describes 175 Skills across Core, Foundry, Python, .NET, TypeScript, Java, and Rust, plus custom agents and MCP configurations. It is explicitly marked work in progress and advises selective loading.
- Microsoft Azure Skills packages Azure workflows with Azure MCP and Foundry MCP connectivity. Its README describes live Azure tools across many Azure services; actual operations require user-authorized Azure account access and may incur provider charges.
- MicrosoftDocs Agent Skills describes 193+ Azure service Skills generated from Microsoft Learn. Skill content is CC BY 4.0 and code is MIT; attribution and exact-scope review are required.
- Microsoft Agent Framework is the current new-build framework reference. The Semantic Kernel README points to it as the successor and provides a migration guide.
- Microsoft Waza is a useful evaluation reference. Its README documents a version boundary between published CLI binaries and newer source changes; do not assume a feature exists in an installed binary until the tagged release is checked.

## Integration plan

1. Use `microsoft/skills` and MicrosoftDocs Agent Skills as candidate catalogues, not as one giant import.
2. Compare domain-specific modules with the existing 22-domain taxonomy; keep only distinct task coverage.
3. Prefer first-party original modules or source references. Redistribute CC BY content only with required attribution, and do not copy unknown-license material.
4. Evaluate Microsoft Agent Framework alongside LangGraph and other orchestrators; do not add two workflow frameworks by default.
5. Use Microsoft Waza concepts for an evaluation harness after verifying its stable release interface.
6. Treat Azure MCP, Foundry MCP, Azure DevOps MCP, and other live connectors as capability providers, not Skills. Require scoped credentials and explicit approval before writes or provisioning.
7. Keep all discoveries in `registry/sources.json`; promote an item to `approved_for_import` only after path-level license, security, compatibility, and test review.

## Duplicate and overlap notes

- `microsoft/skills`, `MicrosoftDocs/agent-skills`, and `microsoft/azure-skills` overlap on Azure/Foundry guidance but serve different purposes: SDK-specific skills, Learn-derived Azure service catalogue, and executable Azure plugin/MCP integration. Keep distinct source records and deduplicate individual modules by task and content.
- `microsoft/agent-framework` and `microsoft/semantic-kernel` are not two default runtime choices. Use Agent Framework for new Microsoft-aligned builds; retain Semantic Kernel knowledge for existing projects and migrations.
- `microsoft/win-dev-skills` overlaps with general software/desktop categories, but its Windows app packaging/debugging expertise is a distinct candidate.
- `microsoft/waza` evaluates workflows; it is not itself a general-purpose orchestration runtime.

## Evidence

- https://github.com/microsoft/skills
- https://github.com/microsoft/azure-skills
- https://github.com/MicrosoftDocs/agent-skills
- https://github.com/microsoft/agent-framework
- https://github.com/microsoft/semantic-kernel
- https://github.com/microsoft/mcp
- https://github.com/microsoft/waza
- https://github.com/microsoft/win-dev-skills
- https://github.com/microsoft/power-platform-skills
- https://github.com/microsoft/cat-agent-skills
- https://github.com/microsoft/azure-devops-mcp
