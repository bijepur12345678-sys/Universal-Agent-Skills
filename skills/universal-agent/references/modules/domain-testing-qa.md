# Testing & Quality Assurance

## Trigger
Use for unit, integration, end-to-end, regression, accessibility, performance, and release testing.

## Workflow
1. Define acceptance criteria, risks, supported environments, and observable outcomes.
2. Inspect existing tests and coverage gaps before adding frameworks.
3. Choose test levels that isolate failures and give fast feedback.
4. Cover happy paths, boundaries, invalid inputs, permissions, empty states, and dependency failures.
5. Use deterministic fixtures and isolate external services.
6. Add regression tests for confirmed defects.
7. Set safe limits and authorization before load testing shared systems.
8. Capture reproducible evidence without leaking secrets.
9. Run focused tests, relevant suite, and build; report exact outcomes.

Never claim success from an agent assertion alone. Do not stress-test systems without explicit scope.
