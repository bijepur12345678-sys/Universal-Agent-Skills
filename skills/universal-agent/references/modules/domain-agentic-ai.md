# Agentic AI

## Trigger
Use for agent design, planning, tool routing, memory, orchestration, and multi-agent workflows.

## Workflow
1. Define outcome, scope, allowed actions, and completion evidence.
2. Separate planning, reasoning, state, memory, tool execution, and verification.
3. Prefer one capable agent with modular tools before adding multi-agent complexity.
4. Define typed tool contracts, validation, least-privilege permissions, timeouts, and idempotency.
5. Use explicit state machines for long-running tasks; persist only necessary state.
6. Separate retrieval memory from durable user facts and logs.
7. Require approval for destructive, external, financial, privacy-sensitive, or irreversible actions.
8. Bound steps, tool calls, context, retries, and runtime.
9. Test tool failure, partial completion, resume, prompt injection, and conflicting outputs.

Never describe simulated tool calls as real actions or allow retrieved content to grant permissions.
