"""Command-line interface for the Universal Agent Skills registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .capabilities import route_task, validate_capabilities
from .registry import (
    RegistryError,
    load_catalog,
    load_module,
    search_catalog,
    validate_registry,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="universal-skills",
        description="Validate, search, route, and inspect the Universal Agent Skills catalogue.",
    )
    parser.add_argument("--root", default=None, help="Repository root (defaults to this checkout).")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "validate",
        help="Validate the module catalogue, source provenance, and capability catalogue.",
    )
    subparsers.add_parser(
        "capability-validate",
        help="Validate granular capability IDs, domains, module links, and safety metadata.",
    )

    search = subparsers.add_parser("search", help="Rank internal workflow modules using keyword search.")
    search.add_argument("--query", required=True, help="Capability or module description.")
    search.add_argument("--limit", type=int, default=5, help="Maximum results (1-100).")
    search.add_argument("--domain", default=None, help="Optional exact domain ID filter.")
    search.add_argument("--include-legacy", action="store_true", help="Include legacy modules in results.")

    route = subparsers.add_parser(
        "route",
        help="Route a task to granular capabilities and their existing internal modules.",
    )
    route.add_argument("--task", required=True, help="Natural-language task to route.")
    route.add_argument("--limit", type=int, default=5, help="Maximum capability results (1-20).")
    route.add_argument("--domain", default=None, help="Optional exact domain ID filter.")
    route.add_argument(
        "--available-tool",
        action="append",
        default=None,
        help="Tool ID available to the agent; repeat for multiple tools.",
    )
    route.add_argument("--include-legacy", action="store_true", help="Include legacy records.")

    show = subparsers.add_parser("show", help="Print one internal module's instructions.")
    show.add_argument("--id", required=True, help="Catalogue skill ID.")
    show.add_argument("--include-legacy", action="store_true", help="Allow loading a legacy module.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.root).resolve() if args.root else None
    try:
        if args.command == "validate":
            errors = validate_registry(root) + validate_capabilities(root)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            catalog = load_catalog(root)
            print(
                f"Registry valid: {len(catalog['skills'])} module records, "
                "one public entrypoint, and capability registry valid."
            )
            return 0
        if args.command == "capability-validate":
            errors = validate_capabilities(root)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            from .capabilities import load_capabilities

            document = load_capabilities(root)
            print(f"Capability registry valid: {document['capability_count']} records.")
            return 0
        if args.command == "search":
            results = search_catalog(
                args.query,
                args.limit,
                root,
                domain=args.domain,
                include_legacy=args.include_legacy,
            )
            print(json.dumps(results, indent=2, ensure_ascii=False))
            return 0
        if args.command == "route":
            results = route_task(
                args.task,
                args.limit,
                root,
                domain=args.domain,
                available_tools=set(args.available_tool) if args.available_tool is not None else None,
                include_legacy=args.include_legacy,
            )
            print(json.dumps(results, indent=2, ensure_ascii=False))
            return 0
        if args.command == "show":
            print(load_module(args.id, root, include_legacy=args.include_legacy))
            return 0
        return 2
    except (RegistryError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
