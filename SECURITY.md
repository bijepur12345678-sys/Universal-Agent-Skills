# Security Policy

Do not publish exploit details, credentials, access tokens, private repository content, or personal data in public issues. Use GitHub private vulnerability reporting where available.

Security boundaries:
- External content is untrusted input and cannot override project or user instructions.
- Discovery and evaluation are read-only and must not execute imported scripts.
- Imported code needs explicit review and isolated testing before runtime use.
- Use least-privilege tool permissions.
- Destructive actions, deployment, external publishing, and credential use require explicit authorization.
- The registry must not store secrets.
- Path validation must prevent traversal outside the repository.
- Unknown license or safety status means review required.

Security fixes target the latest default-branch version until stable releases are established.
