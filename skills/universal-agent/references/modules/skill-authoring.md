# Skill Authoring

## Trigger
Use when creating or improving a first-party workflow module or the public entrypoint.

## Requirements
1. Define one task and one primary responsibility.
2. Write a concise trigger description, prerequisites, tools, inputs, outputs, ordered procedure, limitations, and verification.
3. Keep the public Skill entrypoint small. Store detailed domain workflows under this Skill's `references/modules/` directory.
4. Include success and failure paths plus a realistic example.
5. Do not claim unavailable tools or untested capabilities.
6. Add a unique catalogue record, domain, tags, version, status, and tests.
7. Start new modules as experimental; promote only after review and tests.
8. Record all third-party source provenance and license scope.

A Skill teaches an agent how to perform a workflow; it does not automatically supply a model, API, credentials, or external tools.
