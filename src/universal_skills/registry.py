"""Read-only registry validation, keyword search, and safe module loading."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

_ALLOWED_STATUSES = {"stable", "experimental", "legacy", "deprecated", "archived"}
_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#._-]*", re.IGNORECASE)
_DEFAULT_ROOT = Path(__file__).resolve().parents[2]


class RegistryError(ValueError):
    """Raised when registry data cannot be read or safely resolved."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryError(f"Missing registry file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RegistryError(f"Expected a JSON object in {path}")
    return value


def load_catalog(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root).resolve() if root is not None else _DEFAULT_ROOT
    return _read_json(base / "registry" / "catalog.json")


def load_sources(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root).resolve() if root is not None else _DEFAULT_ROOT
    return _read_json(base / "registry" / "sources.json")


def load_domains(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root).resolve() if root is not None else _DEFAULT_ROOT
    return _read_json(base / "registry" / "domains.json")


def _safe_repo_path(root: Path, relative_path: str) -> Path:
    rel = PurePosixPath(relative_path)
    if rel.is_absolute() or not rel.parts or any(part in {"", ".", ".."} for part in rel.parts):
        raise RegistryError(f"Unsafe repository-relative path: {relative_path!r}")
    resolved_root = root.resolve()
    target = (resolved_root / Path(*rel.parts)).resolve()
    if not target.is_relative_to(resolved_root):
        raise RegistryError(f"Path escapes repository root: {relative_path!r}")
    return target


def validate_registry(root: Path | str | None = None) -> list[str]:
    base = Path(root).resolve() if root is not None else _DEFAULT_ROOT
    errors: list[str] = []
    try:
        catalog = load_catalog(base)
        sources_doc = load_sources(base)
        domains_doc = load_domains(base)
    except RegistryError as exc:
        return [str(exc)]

    for label, document in (("catalog", catalog), ("sources", sources_doc), ("domains", domains_doc)):
        if document.get("schema_version") != 1:
            errors.append(f"{label}.json: schema_version must be 1")

    skills = catalog.get("skills")
    sources = sources_doc.get("sources")
    domains = domains_doc.get("domains")
    if not isinstance(skills, list):
        errors.append("catalog.json: skills must be an array")
        return errors
    if not isinstance(sources, list):
        errors.append("sources.json: sources must be an array")
        return errors
    if not isinstance(domains, list):
        errors.append("domains.json: domains must be an array")
        return errors

    source_ids = {x.get("id") for x in sources if isinstance(x, dict)}
    domain_ids = {x.get("id") for x in domains if isinstance(x, dict)}
    seen_skill_ids: set[str] = set()
    seen_source_ids: set[str] = set()
    seen_domain_ids: set[str] = set()
    entrypoints: list[dict[str, Any]] = []

    for index, skill in enumerate(skills):
        prefix = f"catalog.json: skills[{index}]"
        if not isinstance(skill, dict):
            errors.append(f"{prefix} must be an object")
            continue
        required = ("id", "name", "description", "domain", "path", "version", "status", "tags", "source_ids", "license", "entrypoint")
        for field in required:
            if field not in skill:
                errors.append(f"{prefix} missing required field {field!r}")
        skill_id = skill.get("id")
        if not isinstance(skill_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id):
            errors.append(f"{prefix} has an invalid id")
        elif skill_id in seen_skill_ids:
            errors.append(f"duplicate skill id: {skill_id}")
        else:
            seen_skill_ids.add(skill_id)

        if skill.get("status") not in _ALLOWED_STATUSES:
            errors.append(f"{prefix} has invalid status {skill.get('status')!r}")
        if skill.get("domain") not in domain_ids:
            errors.append(f"{prefix} references unknown domain {skill.get('domain')!r}")
        description = skill.get("description")
        if not isinstance(description, str) or not 20 <= len(description) <= 500:
            errors.append(f"{prefix} description must contain 20 to 500 characters")
        tags = skill.get("tags")
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            errors.append(f"{prefix} tags must be an array of strings")
        source_refs = skill.get("source_ids")
        if not isinstance(source_refs, list):
            errors.append(f"{prefix} source_ids must be an array")
        else:
            for source_id in source_refs:
                if source_id not in source_ids:
                    errors.append(f"{prefix} references unknown source {source_id!r}")
        if skill.get("entrypoint") is True:
            entrypoints.append(skill)

        path = skill.get("path")
        if isinstance(path, str):
            try:
                target = _safe_repo_path(base, path)
                if not target.is_file():
                    errors.append(f"{prefix} path does not exist or is not a file: {path}")
            except RegistryError as exc:
                errors.append(f"{prefix} {exc}")
        else:
            errors.append(f"{prefix} path must be a string")

    if len(entrypoints) != 1:
        errors.append(f"expected exactly one entrypoint record; found {len(entrypoints)}")
    elif catalog.get("entrypoint") != entrypoints[0].get("path"):
        errors.append("catalog.json entrypoint does not match the unique entrypoint skill path")

    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"sources.json: sources[{index}] must be an object")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source_id):
            errors.append(f"sources.json: sources[{index}] has an invalid id")
        elif source_id in seen_source_ids:
            errors.append(f"duplicate source id: {source_id}")
        else:
            seen_source_ids.add(source_id)
        for field in ("url", "type", "license", "license_scope", "review_status", "integration_mode", "use_for", "notes"):
            if field not in source:
                errors.append(f"sources.json: sources[{index}] missing {field!r}")

    for index, domain in enumerate(domains):
        if not isinstance(domain, dict):
            errors.append(f"domains.json: domains[{index}] must be an object")
            continue
        domain_id = domain.get("id")
        if not isinstance(domain_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", domain_id):
            errors.append(f"domains.json: domains[{index}] has an invalid id")
        elif domain_id in seen_domain_ids:
            errors.append(f"duplicate domain id: {domain_id}")
        else:
            seen_domain_ids.add(domain_id)

    return errors


def search_catalog(query: str, limit: int = 5, root: Path | str | None = None) -> list[dict[str, Any]]:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must not be empty")
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")

    catalog = load_catalog(root)
    tokens = set(_TOKEN_RE.findall(query.casefold()))
    phrase = " ".join(query.casefold().split())
    ranked: list[tuple[int, str, dict[str, Any]]] = []

    for skill in catalog.get("skills", []):
        if not isinstance(skill, dict) or skill.get("status") in {"deprecated", "archived"}:
            continue
        fields = {
            "id": str(skill.get("id", "")).casefold(),
            "name": str(skill.get("name", "")).casefold(),
            "description": str(skill.get("description", "")).casefold(),
            "domain": str(skill.get("domain", "")).casefold(),
            "tags": " ".join(str(tag).casefold() for tag in skill.get("tags", [])),
        }
        score = 0
        if phrase in fields["name"]:
            score += 8
        if phrase in fields["description"]:
            score += 5
        for token in tokens:
            if token in fields["id"]:
                score += 5
            if token in fields["name"]:
                score += 4
            if token in fields["tags"]:
                score += 3
            if token in fields["domain"]:
                score += 2
            if token in fields["description"]:
                score += 1
        if score:
            ranked.append((score, str(skill.get("id", "")), skill))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:limit]]


def load_module(skill_id: str, root: Path | str | None = None, include_legacy: bool = False) -> str:
    base = Path(root).resolve() if root is not None else _DEFAULT_ROOT
    catalog = load_catalog(base)
    matches = [item for item in catalog.get("skills", []) if isinstance(item, dict) and item.get("id") == skill_id]
    if not matches:
        raise RegistryError(f"Unknown skill id: {skill_id}")
    skill = matches[0]
    status = skill.get("status")
    if status in {"deprecated", "archived"} or (status == "legacy" and not include_legacy):
        raise RegistryError(f"Skill {skill_id!r} is not loadable by default (status={status!r})")
    path = skill.get("path")
    if not isinstance(path, str):
        raise RegistryError(f"Skill {skill_id!r} has no valid path")
    target = _safe_repo_path(base, path)
    if not target.is_file():
        raise RegistryError(f"Skill content not found: {path}")
    return target.read_text(encoding="utf-8")
