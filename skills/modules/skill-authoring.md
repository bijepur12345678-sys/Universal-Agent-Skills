# Internal Module: Skill Authoring

## Trigger
Use when creating or improving first-party Skill instructions or internal workflow modules.

## Requirements
1. Define one clear user task and one primary responsibility.
2. Use a precise description explaining when the module should trigger.
3. The single public entrypoint uses Agent Skills format: a directory with `SKILL.md` and YAML frontmatter containing `name` and `description`.
4. Keep internal domain instructions as ordinary reference Markdown, not additional top-level Skills.
5. Document prerequisites, tools, inputs, outputs, steps, limitations, failure paths, and verification.
6. Include a realistic example and a non-trigger example where ambiguity is likely.
7. Do not claim universal or autonomous capability without evidence.
8. Keep the entrypoint concise and load domain details lazily.
9. Add a catalogue record and tests for IDs, paths, domains, sources, and routing.
10. Version behavioral changes and update the changelog.

## Quality checklist
Instructions are actionable; tool availability is not assumed; no secrets are embedded; provenance is recorded; the module does not duplicate another responsibility.
