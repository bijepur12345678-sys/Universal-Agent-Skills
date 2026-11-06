# Internal Module Index

This file belongs to the `universal-agent` Skill package. Select only the modules needed for the current task.

| Module ID | File | Trigger |
|---|---|---|
| `github-source-research` | `modules/github-source-research.md` | Find and evaluate public repositories, releases, compatibility, maintenance, security, and license evidence for candidate skills and tools. |
| `skill-authoring` | `modules/skill-authoring.md` | Create modular and testable Agent Skills instructions with metadata, triggers, prerequisites, examples, and validation guidance. |
| `license-provenance-review` | `modules/license-provenance-review.md` | Review file-level license scope, source revisions, attribution, notices, and redistribution constraints before including third-party materials. |
| `registry-maintenance` | `modules/registry-maintenance.md` | Maintain unique skill IDs, metadata quality, domain membership, source references, versions, and lifecycle status in the canonical catalogue. |
| `domain-ai-ml` | `modules/domain-ai-ml.md` | Handle LLMs, embeddings, RAG, model selection, evaluation, fine-tuning, inference, and ML workflows. |
| `domain-agentic-ai` | `modules/domain-agentic-ai.md` | Design agents, planning, tool routing, memory, stateful workflows, orchestration, and multi-agent systems. |
| `domain-software-engineering` | `modules/domain-software-engineering.md` | Implement, debug, refactor, review, and maintain software repositories, APIs, and application architecture. |
| `domain-frontend` | `modules/domain-frontend.md` | Build responsive accessible interfaces, components, UI state, design systems, and frontend performance improvements. |
| `domain-backend` | `modules/domain-backend.md` | Design and implement APIs, backend services, authentication, authorization, jobs, and service integrations. |
| `domain-cloud` | `modules/domain-cloud.md` | Plan and operate cloud architectures, serverless applications, Workers, storage, networking, and hosted services. |
| `domain-devops` | `modules/domain-devops.md` | Build CI/CD pipelines, containers, infrastructure automation, deployment, monitoring, and reliability workflows. |
| `domain-databases` | `modules/domain-databases.md` | Design schemas, SQL and PostgreSQL queries, migrations, indexes, access policies, and data recovery workflows. |
| `domain-research` | `modules/domain-research.md` | Conduct source-grounded research, repository discovery, evidence synthesis, literature review, and fact-checking. |
| `domain-ui-ux` | `modules/domain-ui-ux.md` | Design user journeys, wireframes, prototypes, design systems, usable interfaces, and accessible experiences. |
| `domain-browser` | `modules/domain-browser.md` | Inspect websites and automate authorized browser workflows using accessible page structure and verified state. |
| `domain-desktop` | `modules/domain-desktop.md` | Inspect and automate authorized desktop applications using semantic UI Automation and accessibility interfaces. |
| `domain-mobile` | `modules/domain-mobile.md` | Build and test Android and iOS applications, mobile interfaces, permissions, Flutter, and React Native workflows. |
| `domain-media` | `modules/domain-media.md` | Plan and review image, video, audio, speech, transcription, editing, and creative asset workflows. |
| `domain-youtube` | `modules/domain-youtube.md` | Research public YouTube channels and video metadata, analyze authorized analytics, and plan content workflows. |
| `domain-automation` | `modules/domain-automation.md` | Design API, MCP, webhook, scheduled, and cross-application workflows with secure authorization and retries. |
| `domain-documents` | `modules/domain-documents.md` | Extract, transform, generate, and verify PDF, Word, Excel, PowerPoint, Markdown, and structured reports. |
| `domain-data-science` | `modules/domain-data-science.md` | Clean, analyze, visualize, and transform data using reproducible statistical, ETL, and analytics workflows. |
| `domain-security-analysis` | `modules/domain-security-analysis.md` | Review code and dependencies, assess defensive security risks, and analyze owned or explicitly authorized software. |
| `domain-testing-qa` | `modules/domain-testing-qa.md` | Plan and run unit, integration, end-to-end, accessibility, performance, and regression tests. |
| `domain-education` | `modules/domain-education.md` | Create age-appropriate explanations, tutoring workflows, practice materials, and curriculum-aware learning resources. |
| `domain-business` | `modules/domain-business.md` | Support product planning, process design, market research, project operations, and business documentation. |

## Loading policy

- Load one to five relevant modules for a normal task.
- Multi-stage tasks may combine distinct modules in a clear order.
- Do not load all modules into context.
- Use the repository-level `registry/catalog.json` for lifecycle status, source provenance, tags, and dependencies when available.
- New modules are experimental until tests and review justify promotion.
