# Upstream Source and Import Policy

## Review states
- `reviewed_reference`: source metadata and relevant documentation inspected; suitable as a reference.
- `reference_only`: link to the source; do not copy content.
- `review_required`: evidence incomplete; do not import.
- `approved_for_import`: exact file scope, license, attribution and security review passed.
- `rejected`: unsuitable due to license, security, quality or relevance.

## Import gates
Verify the exact file, author, immutable revision, applicable license, nested notices, redistribution rights, dependencies, executable scripts, network access, credentials, maintenance, compatibility and overlap.

## Defaults
Unknown license means reference-only. Source-available material is not redistributable by default. Mixed-license repositories require path-by-path review. Never execute imported scripts during discovery. New candidates enter review and are never automatically activated.


## Special license-scope examples

- MicrosoftDocs Agent Skills uses a dual license: Skill/documentation content is CC BY 4.0 and code is MIT. Preserve attribution and use the exact license that applies to each path.
- Community skill galleries and aggregate repositories may contain third-party contributions. A repository-level MIT license is not sufficient evidence that every contributed Skill or asset is redistributable.
- Microsoft source candidates with unverified license status remain `review_required`; do not copy or activate them until the license is verified.
