"""Granular capability catalogue validation and deterministic task routing."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .registry import RegistryError, load_catalog, load_domains

_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#._-]*", re.IGNORECASE)
_ALLOWED_STATUS = {"stable", "experimental", "legacy", "deprecated", "archived"}
_ALLOWED_RISK = {"low", "moderate", "elevated"}
_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "build", "by", "do", "for",
    "from", "get", "how", "i", "in", "is", "it", "make", "me", "my", "of",
    "on", "or", "please", "set", "that", "the", "this", "to", "use", "with",
}


def _root(root: Path | str | None = None) -> Path:
    return Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]


def load_capabilities(root: Path | str | None = None) -> dict[str, Any]:
    """Load the canonical granular capability catalogue."""
    path = _root(root) / "registry" / "capabilities.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryError(f"Missing capability registry: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RegistryError("capabilities.json must contain a JSON object")
    return value


def validate_capabilities(root: Path | str | None = None) -> list[str]:
    """Validate capability IDs, domain/module links, metadata, and safety gates."""
    base = _root(root)
    errors: list[str] = []
    try:
        document = load_capabilities(base)
        catalog = load_catalog(base)
        domains_doc = load_domains(base)
    except RegistryError as exc:
        return [str(exc)]

    if document.get("schema_version") != 1:
        errors.append("capabilities.json: schema_version must be 1")
    records = document.get("capabilities")
    if not isinstance(records, list):
        return errors + ["capabilities.json: capabilities must be an array"]
    if document.get("capability_count") != len(records):
        errors.append("capabilities.json: capability_count does not match the array length")

    domain_ids = {
        item.get("id") for item in domains_doc.get("domains", [])
        if isinstance(item, dict)
    }
    modules = {
        item.get("id"): item for item in catalog.get("skills", [])
        if isinstance(item, dict)
    }
    seen_ids: set[str] = set()
    seen_signatures: set[tuple[str, tuple[str, ...]]] = set()

    for index, item in enumerate(records):
        prefix = f"capabilities.json: capabilities[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in (
            "id", "domain", "module_id", "name", "description", "triggers",
            "synonyms", "required_tools", "risk_level", "approval_required", "status", "workflow_ref",
        ):
            if field not in item:
                errors.append(f"{prefix} missing {field!r}")

        capability_id = item.get("id")
        if not isinstance(capability_id, str) or not _ID_RE.fullmatch(capability_id):
            errors.append(f"{prefix} has an invalid ID")
        elif capability_id in seen_ids:
            errors.append(f"duplicate capability ID: {capability_id}")
        else:
            seen_ids.add(capability_id)

        domain = item.get("domain")
        if domain not in domain_ids:
            errors.append(f"{prefix} references unknown domain {domain!r}")

        module_id = item.get("module_id")
        module = modules.get(module_id)
        if module is None or module.get("entrypoint") is True:
            errors.append(f"{prefix} references unknown internal module {module_id!r}")
        elif module.get("domain") != domain:
            errors.append(f"{prefix} domain does not match module {module_id!r}")

        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix} name must be a non-empty string")
        description = item.get("description")
        if not isinstance(description, str) or len(description.strip()) < 30:
            errors.append(f"{prefix} description must contain at least 30 characters")

        for field in ("triggers", "synonyms", "required_tools"):
            values = item.get(field)
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value.strip() for value in values
            ):
                errors.append(f"{prefix} {field} must be an array of non-empty strings")
            elif len(values) != len(set(values)):
                errors.append(f"{prefix} {field} contains duplicate values")

        triggers = item.get("triggers")
        if isinstance(triggers, list):
            normalized = tuple(sorted(" ".join(value.casefold().split()) for value in triggers if isinstance(value, str)))
            signature = (str(domain), normalized)
            if signature in seen_signatures:
                errors.append(f"{prefix} duplicates a trigger signature in domain {domain!r}")
            seen_signatures.add(signature)

        if item.get("risk_level") not in _ALLOWED_RISK:
            errors.append(f"{prefix} has invalid risk_level {item.get('risk_level')!r}")
        if item.get("status") not in _ALLOWED_STATUS:
            errors.append(f"{prefix} has invalid status {item.get('status')!r}")
        if not isinstance(item.get("approval_required"), bool):
            errors.append(f"{prefix} approval_required must be a boolean")
        elif item.get("risk_level") == "elevated" and item.get("approval_required") is not True:
            errors.append(f"{prefix} elevated-risk capability must require approval")

    workflow_path = base / "skills" / "universal-agent" / "references" / "capability-workflows.md"
    if not workflow_path.is_file():
        errors.append("missing capability workflow pack: skills/universal-agent/references/capability-workflows.md")
    else:
        try:
            workflow_text = workflow_path.read_text(encoding="utf-8")
            for index, item in enumerate(records):
                if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                    continue
                capability_id = item["id"]
                expected_ref = "skills/universal-agent/references/capability-workflows.md#" + capability_id
                if item.get("workflow_ref") != expected_ref:
                    errors.append(
                        f"capabilities.json: capabilities[{index}] has an invalid workflow_ref"
                    )
                    continue
                heading = re.compile(r"(?m)^## " + re.escape(capability_id) + r" — .+$")
                if not heading.search(workflow_text):
                    errors.append(
                        f"capabilities.json: capabilities[{index}] workflow section is missing"
                    )
        except OSError as exc:
            errors.append(f"unable to read capability workflow pack: {exc}")

    return errors


def load_capability_workflow(
    capability_id: str,
    root: Path | str | None = None,
    include_legacy: bool = False,
) -> str:
    """Load one capability's section without loading unrelated workflow instructions."""
    if not isinstance(capability_id, str) or not _ID_RE.fullmatch(capability_id):
        raise ValueError("capability_id must be a lowercase stable ID")

    document = load_capabilities(root)
    matches = [
        item for item in document.get("capabilities", [])
        if isinstance(item, dict) and item.get("id") == capability_id
    ]
    if not matches:
        raise RegistryError(f"Unknown capability ID: {capability_id}")

    record = matches[0]
    status = record.get("status")
    if status in {"deprecated", "archived"} or (status == "legacy" and not include_legacy):
        raise RegistryError(
            f"Capability {capability_id!r} is not loadable by default (status={status!r})"
        )

    expected_ref = "skills/universal-agent/references/capability-workflows.md#" + capability_id
    if record.get("workflow_ref") != expected_ref:
        raise RegistryError(f"Capability {capability_id!r} has an invalid workflow reference")

    workflow_path = (
        _root(root) / "skills" / "universal-agent" / "references" / "capability-workflows.md"
    )
    try:
        content = workflow_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RegistryError("Capability workflow pack is missing") from exc

    match = re.search(r"(?m)^## " + re.escape(capability_id) + r" — .+$", content)
    if not match:
        raise RegistryError(f"Capability workflow section not found: {capability_id}")
    next_heading = re.search(r"(?m)^## ", content[match.end():])
    end = match.end() + next_heading.start() if next_heading else len(content)
    return content[match.start():end].strip()


def _tokens(value: str) -> set[str]:
    return {
        token.casefold()
        for token in _TOKEN_RE.findall(value)
        if token.casefold() not in _STOP_WORDS and len(token) > 1
    }


def route_task(
    task: str,
    limit: int = 5,
    root: Path | str | None = None,
    domain: str | None = None,
    available_tools: set[str] | None = None,
    include_legacy: bool = False,
) -> list[dict[str, Any]]:
    """Return a ranked, explainable list of matching capability records."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must not be empty")
    if not isinstance(limit, int) or not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")
    if domain is not None and not _ID_RE.fullmatch(domain):
        raise ValueError("domain must be a lowercase domain ID")

    document = load_capabilities(root)
    catalog = load_catalog(root)
    module_by_id = {
        item.get("id"): item for item in catalog.get("skills", [])
        if isinstance(item, dict)
    }
    query = " ".join(task.casefold().split())
    query_tokens = _tokens(task)
    results: list[dict[str, Any]] = []

    for item in document.get("capabilities", []):
        if not isinstance(item, dict):
            continue
        status = item.get("status")
        if status in {"deprecated", "archived"} or (status == "legacy" and not include_legacy):
            continue
        if domain is not None and item.get("domain") != domain:
            continue
        module = module_by_id.get(item.get("module_id"))
        if not module:
            continue
        module_status = module.get("status")
        if module_status in {"deprecated", "archived"} or (
            module_status == "legacy" and not include_legacy
        ):
            continue

        name = str(item.get("name", "")).casefold()
        description = str(item.get("description", "")).casefold()
        triggers = [str(value).casefold() for value in item.get("triggers", [])]
        synonyms = [str(value).casefold() for value in item.get("synonyms", [])]
        trigger_tokens = set().union(*(_tokens(value) for value in triggers)) if triggers else set()
        synonym_tokens = set().union(*(_tokens(value) for value in synonyms)) if synonyms else set()
        name_tokens = _tokens(name)
        description_tokens = _tokens(description)

        score = 0
        matched_terms: list[str] = []
        for phrase in triggers:
            if phrase and phrase in query:
                score += 12
                matched_terms.append(phrase)
        for phrase in synonyms:
            if phrase and phrase in query:
                score += 7
                matched_terms.append(phrase)
        if name and name in query:
            score += 10
            matched_terms.append(name)

        for token in query_tokens:
            if token in name_tokens:
                score += 4
                matched_terms.append(token)
            if token in trigger_tokens:
                score += 3
                matched_terms.append(token)
            if token in synonym_tokens:
                score += 2
                matched_terms.append(token)
            if token in description_tokens:
                score += 1

        if not score:
            continue
        if status == "stable" and module_status == "stable":
            score += 3

        required = set(item.get("required_tools", []))
        missing = sorted(required - available_tools) if available_tools is not None else []
        results.append({
            "capability_id": item["id"],
            "name": item["name"],
            "domain": item["domain"],
            "module_id": item["module_id"],
            "status": status,
            "module_status": module_status,
            "score": score,
            "matched_terms": sorted(set(matched_terms)),
            "required_tools": sorted(required),
            "missing_tools": missing,
            "tools_ready": not missing if available_tools is not None else None,
            "risk_level": item["risk_level"],
            "approval_required": item["approval_required"],
        })

    results.sort(key=lambda value: (-value["score"], value["capability_id"]))
    return results[:limit]
