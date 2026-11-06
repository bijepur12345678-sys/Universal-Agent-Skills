# Domain Module: Software Engineering

## Trigger
Use for software design, implementation, debugging, refactoring, code review, API work, or repository maintenance.

## Workflow
1. Inspect the existing repository, instructions, tests, framework versions, and current changes before editing.
2. Translate the request into observable behavior and acceptance tests.
3. Trace the relevant call paths and preserve established project conventions.
4. Add or update a focused failing test where practical, then make the smallest correct change.
5. Keep interfaces typed and errors explicit; avoid unrelated refactoring.
6. Consider security, accessibility, performance, compatibility, and migration impact.
7. Run the focused tests, full relevant suite, formatter/linter, and build when available.
8. Review the diff for accidental changes, secrets, generated noise, and missing documentation.
9. Report files changed, commands run, test outcomes, and any unresolved limitations.

## Outputs
A focused implementation or review with tests and reproducible verification evidence.

## Boundaries
Do not claim tests pass without their output. Do not overwrite user changes or force-push without explicit authorization.
