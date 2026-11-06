# Registry Maintenance

## Trigger
Use when adding, updating, deprecating, or auditing catalogue and source records.

## Lifecycle
1. Create/verify a source record before adding a source-derived module.
2. Check unique ID, semantic overlap, tags, domain, dependencies, and target task.
3. Validate path, version, status, source IDs, license, and content.
4. Start as experimental; promote only after tests and review.
5. Preserve version history. Mark superseded content legacy/deprecated with a replacement reason.
6. Rebuild deterministic indexes and run validators.

## Duplicate policy
Exact duplicates use one canonical ID and retained aliases. Near-duplicates require comparison of task, triggers, workflow, and evidence before merging. Complementary modules remain distinct.

## Scale
Keep metadata compact; lazy-load instructions. Shard domain packages only when scale requires it. Store large binary assets outside Git history with checksums and provenance.
