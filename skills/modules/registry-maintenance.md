# Internal Module: Registry Maintenance

## Trigger
Use when adding, updating, deprecating, or auditing catalogue entries and source records.

## Lifecycle
1. Create a source record before a skill record.
2. Check exact ID, semantic overlap, tags, domain, and intended user task.
3. Validate content path, metadata, dependencies, source IDs, license, and status.
4. New modules start as `experimental`; promote only after focused tests and review.
5. Keep old versions traceable. Do not silently overwrite or delete referenced versions.
6. Mark superseded modules `legacy` or `deprecated` with a replacement and reason.
7. Rebuild indexes deterministically and run all validators.

## Duplicate policy
- Exact duplicate: same normalized content and source identity; retain one canonical record and preserve aliases.
- Near duplicate: overlapping task, triggers, and workflow; compare evidence and merge only after review.
- Complementary modules remain separate when responsibilities or workflow stages differ.
- Similar names alone are not grounds for merging.

## Scale
Keep metadata compact. Partition package content by domain only when repository/API scale requires it. Large assets belong in separately versioned storage with checksums and provenance, not Git history.
