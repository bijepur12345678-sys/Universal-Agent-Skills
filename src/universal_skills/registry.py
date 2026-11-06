"""Registry validation, ranked search, and safe module loading."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

_ALLOWED_STATUSES = {"stable", "experimental", "legacy", "deprecated", "archived"}
_ALLOWED_SOURCE_REVIEW = {"reviewed_reference", "reference_only", "review_required", "approved_for_import", "rejected"}
_ALLOWED_SOURCE_TYPES = {"github_repository", "official_documentation"}
_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#._-]*", re.IGNORECASE)
_ID_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_VERSION_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?")
_DEFAULT_ROOT = Path(__file__).resolve().parents[2]
_PACKAGE_MODULE_PREFIX = "skills/universal-agent/references/modules/"


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
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise RegistryError("Repository-relative path must be a non-empty string")
    if "\\" in relative_path or "\x00" in relative_path or re.match(r"^[A-Za-z]:", relative_path):
        raise RegistryError(f"Unsafe repository-relative path: {relative_path!r}")
    rel = PurePosixPath(relative_path)
    if rel.is_absolute() or not rel.parts or any(part in {"", ".", ".."} for part in rel.parts):
        raise RegistryError(f"Unsafe repository-relative path: {relative_path!r}")
    resolved_root = root.resolve()
    target = (resolved_root / Path(*rel.parts)).resolve()
    if not target.is_relative_to(resolved_root):
        raise RegistryError(f"Path escapes repository root: {relative_path!r}")
    return target


def validate_registry(root: Path | str | None = None) -> list[str]:
    """Return all detected registry integrity errors without executing content."""
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
        return errors + ["catalog.json: skills must be an array"]
    if not isinstance(sources, list):
        return errors + ["sources.json: sources must be an array"]
    if not isinstance(domains, list):
        return errors + ["domains.json: domains must be an array"]

    source_ids = {item.get("id") for item in sources if isinstance(item, dict)}
    domain_ids = {item.get("id") for item in domains if isinstance(item, dict)}
    seen_skill_ids: set[str] = set()
    seen_source_ids: set[str] = set()
    seen_domain_ids: set[str] = set()
    seen_paths: set[str] = set()
    content_digests: dict[str, str] = {}
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
        if not isinstance(skill_id, str) or not _ID_RE.fullmatch(skill_id):
            errors.append(f"{prefix} has an invalid id")
        elif skill_id in seen_skill_ids:
            errors.append(f"duplicate skill id: {skill_id}")
        else:
            seen_skill_ids.add(skill_id)

        name = skill.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix} name must be a non-empty string")
        if skill.get("status") not in _ALLOWED_STATUSES:
            errors.append(f"{prefix} has invalid status {skill.get('status')!r}")
        if skill.get("domain") not in domain_ids:
            errors.append(f"{prefix} references unknown domain {skill.get('domain')!r}")
        description = skill.get("description")
        if not isinstance(description, str) or not 20 <= len(description) <= 500:
            errors.append(f"{prefix} description must contain 20 to 500 characters")
        version = skill.get("version")
        if not isinstance(version, str) or not _VERSION_RE.fullmatch(version):
            errors.append(f"{prefix} has invalid semantic version {version!r}")
        license_name = skill.get("license")
        if not isinstance(license_name, str) or not license_name.strip():
            errors.append(f"{prefix} license must be a non-empty string")

        tags = skill.get("tags")
        if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
            errors.append(f"{prefix} tags must be an array of non-empty strings")
        elif len(tags) != len(set(tags)):
            errors.append(f"{prefix} contains duplicate tags")

        source_refs = skill.get("source_ids")
        if not isinstance(source_refs, list):
            errors.append(f"{prefix} source_ids must be an array")
        else:
            if len(source_refs) != len(set(source_refs)):
                errors.append(f"{prefix} contains duplicate source IDs")
            for source_id in source_refs:
                if source_id not in source_ids:
                    errors.append(f"{prefix} references unknown source {source_id!r}")

        entrypoint_value = skill.get("entrypoint")
        if not isinstance(entrypoint_value, bool):
            errors.append(f"{prefix} entrypoint must be a boolean")
        elif entrypoint_value:
            entrypoints.append(skill)

        path = skill.get("path")
        if isinstance(path, str):
            if path in seen_paths:
                errors.append(f"duplicate catalogue path: {path}")
            seen_paths.add(path)
            if entrypoint_value is False and not path.startswith(_PACKAGE_MODULE_PREFIX):
                errors.append(f"{prefix} internal module must be inside the public Skill package")
            try:
                target = _safe_repo_path(base, path)
                if not target.is_file():
                    errors.append(f"{prefix} path does not exist or is not a file: {path}")
                else:
                    digest = hashlib.sha256(target.read_bytes()).hexdigest()
                    previous = content_digests.get(digest)
                    if previous is not None:
                        errors.append(f"{prefix} duplicates content already referenced by {previous}")
                    else:
                        content_digests[digest] = str(skill_id)
            except (RegistryError, OSError) as exc:
                errors.append(f"{prefix} {exc}")
        else:
            errors.append(f"{prefix} path must be a string")

    if len(entrypoints) != 1:
        errors.append(f"expected exactly one entrypoint record; found {len(entrypoints)}")
    elif catalog.get("entrypoint") != entrypoints[0].get("path"):
        errors.append("catalog.json entrypoint does not match the unique entrypoint skill path")

    for index, source in enumerate(sources):
        prefix = f"sources.json: sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix} must be an object")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not _ID_RE.fullmatch(source_id):
            errors.append(f"{prefix} has an invalid id")
        elif source_id in seen_source_ids:
            errors.append(f"duplicate source id: {source_id}")
        else:
            seen_source_ids.add(source_id)

        for field in ("url", "type", "license", "license_scope", "review_status", "integration_mode", "use_for", "notes"):
            if field not in source:
                errors.append(f"{prefix} missing {field!r}")
        url = source.get("url")
        parsed_url = urlparse(url) if isinstance(url, str) else None
        if parsed_url is None or parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            errors.append(f"{prefix} has an invalid HTTP(S) URL")
        if source.get("type") not in _ALLOWED_SOURCE_TYPES:
            errors.append(f"{prefix} has invalid source type {source.get('type')!r}")
        if source.get("review_status") not in _ALLOWED_SOURCE_REVIEW:
            errors.append(f"{prefix} has invalid review status {source.get('review_status')!r}")
        use_for = source.get("use_for")
        if not isinstance(use_for, list) or not all(isinstance(value, str) and value.strip() for value in use_for):
            errors.append(f"{prefix} use_for must be an array of non-empty strings")
        if not isinstance(source.get("notes"), str):
            errors.append(f"{prefix} notes must be a string")

    for index, domain in enumerate(domains):
        prefix = f"domains.json: domains[{index}]"
        if not isinstance(domain, dict):
            errors.append(f"{prefix} must be an object")
            continue
        domain_id = domain.get("id")
        if not isinstance(domain_id, str) or not _ID_RE.fullmatch(domain_id):
            errors.append(f"{prefix} has an invalid id")
        elif domain_id in seen_domain_ids:
            errors.append(f"duplicate domain id: {domain_id}")
        else:
            seen_domain_ids.add(domain_id)
        if not isinstance(domain.get("name"), str) or not domain.get("name", "").strip():
            errors.append(f"{prefix} name must be a non-empty string")
        if not isinstance(domain.get("description"), str) or not domain.get("description", "").strip():
            errors.append(f"{prefix} description must be a non-empty string")

    return errors


def search_catalog(
    query: str,
    limit: int = 5,
    root: Path | str | None = None,
    domain: str | None = None,
    include_legacy: bool = False,
) -> list[dict[str, Any]]:
    """Rank catalogue records with deterministic keyword search."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must not be empty")
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    if domain is not None and not _ID_RE.fullmatch(domain):
        raise ValueError("domain must be a lowercase domain ID")

    catalog = load_catalog(root)
    tokens = set(_TOKEN_RE.findall(query.casefold()))
    phrase = " ".join(query.casefold().split())
    ranked: list[tuple[int, str, dict[str, Any]]] = []

    for skill in catalog.get("skills", []):
        if not isinstance(skill, dict):
            continue
        status = skill.get("status")
        if status in {"deprecated", "archived"} or (status == "legacy" and not include_legacy):
            continue
        if domain is not None and skill.get("domain") != domain:
            continue
        fields = {
            "id": str(skill.get("id", "")).casefold(),
            "name": str(skill.get("name", "")).casefold(),
            "description": str(skill.get("description", "")).casefold(),
            "domain": str(skill.get("domain", "")).casefold(),
            "tags": " ".join(str(tag).casefold() for tag in skill.get("tags", [])),
        }
        score = 0
        if phrase and phrase in fields["name"]:
            score += 8
        if phrase and phrase in fields["description"]:
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
        if status == "stable":
            score += 2
        if score:
            ranked.append((score, str(skill.get("id", "")), skill))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:limit]]


def load_module(skill_id: str, root: Path | str | None = None, include_legacy: bool = False) -> str:
    """Load one reviewed internal module while enforcing repository path safety."""
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
