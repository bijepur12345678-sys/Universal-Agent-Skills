"""Command-line interface for the Universal Agent Skills registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .registry import RegistryError, load_catalog, load_module, search_catalog, validate_registry


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="universal-skills", description="Validate and search the Universal Agent Skills catalogue.")
    parser.add_argument("--root", default=None, help="Repository root (defaults to the checked-out project root).")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate catalogue IDs, references, and content paths.")
    search = subparsers.add_parser("search", help="Search the catalogue using lightweight keyword matching.")
    search.add_argument("--query", required=True, help="Task or capability description.")
    search.add_argument("--limit", type=int, default=5, help="Maximum results (1-100).")
    show = subparsers.add_parser("show", help="Print one module's instructions.")
    show.add_argument("--id", required=True, help="Catalogue skill ID.")
    show.add_argument("--include-legacy", action="store_true", help="Allow loading a legacy module.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.root).resolve() if args.root else None
    try:
        if args.command == "validate":
            errors = validate_registry(root)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            catalog = load_catalog(root)
            print(f"Registry valid: {len(catalog['skills'])} skills; one entrypoint.")
            return 0
        if args.command == "search":
            print(json.dumps(search_catalog(args.query, args.limit, root), indent=2, ensure_ascii=False))
            return 0
        if args.command == "show":
            print(load_module(args.id, root, include_legacy=args.include_legacy))
            return 0
        return 2
    except (RegistryError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
