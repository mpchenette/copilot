#!/usr/bin/env python3
"""
find_json_string.py

Search a JSON file for occurrences of a string (or regex) and output the
1-based line numbers where matches occur. Works on the raw file text so it
doesn't require valid JSON and preserves line numbers.

Usage:
  python3 scripts/find_json_string.py path/to/file.json "needle"

Options:
  -i, --ignore-case   Case-insensitive search
  -r, --regex         Treat the pattern as a regular expression
  -w, --word          Whole-word match (implies regex with word boundaries)
  -N, --numbers-only  Print only numbers, one per line (default)
  -l, --list          Print "line: content" for each matching line

Examples:
  python3 scripts/find_json_string.py data.json "user_id"
  python3 scripts/find_json_string.py data.json "error .* timeout" -r -i -l
  cat data.json | python3 scripts/find_json_string.py - "foo" -w
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import Iterable, List


def iter_lines(path: str) -> Iterable[tuple[int, str]]:
    if path == "-":
        for i, line in enumerate(sys.stdin, start=1):
            yield i, line.rstrip("\n")
        return
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, start=1):
                yield i, line.rstrip("\n")
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"error: cannot read {path}: {e}", file=sys.stderr)
        sys.exit(2)


def find_matches(
    lines: Iterable[tuple[int, str]],
    pattern: str,
    ignore_case: bool = False,
    regex: bool = False,
    whole_word: bool = False,
) -> List[int]:
    flags = re.IGNORECASE if ignore_case else 0
    if whole_word:
        regex = True
        pattern = rf"\b{re.escape(pattern)}\b"

    compiled = None
    if regex:
        try:
            compiled = re.compile(pattern, flags)
        except re.error as e:
            print(f"error: invalid regex: {e}", file=sys.stderr)
            sys.exit(2)

    hits: List[int] = []
    if compiled is not None:
        for ln, text in lines:
            if compiled.search(text) is not None:
                hits.append(ln)
    else:
        if ignore_case:
            needle = pattern.lower()
            for ln, text in lines:
                if needle in text.lower():
                    hits.append(ln)
        else:
            for ln, text in lines:
                if pattern in text:
                    hits.append(ln)

    # De-duplicate while preserving order
    seen = set()
    unique_hits: List[int] = []
    for ln in hits:
        if ln not in seen:
            seen.add(ln)
            unique_hits.append(ln)
    return unique_hits


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Find lines in a JSON file containing a string or regex.",
    )
    p.add_argument(
        "path",
        help="Path to JSON file, or '-' for stdin",
    )
    p.add_argument(
        "pattern",
        help="Search string (or regex with -r)",
    )
    p.add_argument(
        "-i",
        "--ignore-case",
        action="store_true",
        help="Case-insensitive search",
    )
    p.add_argument(
        "-r",
        "--regex",
        action="store_true",
        help="Treat pattern as a regular expression",
    )
    p.add_argument(
        "-w",
        "--word",
        action="store_true",
        help="Whole-word match (wraps pattern with word boundaries)",
    )
    output = p.add_mutually_exclusive_group()
    output.add_argument(
        "-N",
        "--numbers-only",
        action="store_true",
        help="Print only line numbers (default)",
    )
    output.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="Print 'line: content' for each matching line",
    )

    args = p.parse_args(argv)

    hits = find_matches(
        iter_lines(args.path),
        args.pattern,
        ignore_case=args.ignore_case,
        regex=args.regex,
        whole_word=args.word,
    )

    if args.list:
        # Re-iterate lines for printing content efficiently
        line_set = set(hits)
        for ln, text in iter_lines(args.path):
            if ln in line_set:
                print(f"{ln}: {text}")
    else:
        for ln in hits:
            print(ln)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

