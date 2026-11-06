# Contributing

Useful contributions include first-party modules, registry improvements, source reviews, compatibility adapters, and reproducible tests.

Before proposing a module:
1. Search for an existing capability or near-duplicate.
2. Define one task and one primary responsibility.
3. Add triggers, prerequisites, tools, inputs, outputs, limitations, examples, and verification.
4. Record domain, version, lifecycle status, source IDs, and license.
5. For third-party material, provide exact file URL, commit/tag, author, license, and required notices.
6. Do not copy material if redistribution rights are unclear.

Pull request checklist:
- [ ] No credentials or private data.
- [ ] No imported script is executed during discovery or validation.
- [ ] IDs and paths are valid; duplicates are checked.
- [ ] License and provenance are recorded.
- [ ] Focused tests cover success and failure cases.
- [ ] Documentation describes compatibility and limitations.
- [ ] Full validation commands pass.

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
python -m universal_skills validate
```

All contributions require review. A catalogue entry is not automatically trusted or production-ready.
