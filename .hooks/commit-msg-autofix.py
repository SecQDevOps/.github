#!/usr/bin/env python3
"""Auto-fix a commit message in place (wired as a pre-commit ``commit-msg`` hook).

This hook never rejects; it repairs what it can and logs each change to stderr,
leaving the rest for commitlint to validate. Two fixes are applied:

1. **Strip attribution / AI-authorship trailers** — ``Co-authored-by``,
   ``Co-worked-by`` / ``Co-worked by``, ``Generated with|by …``, and any line
   containing the robot emoji. Genuine trailers (``Reviewed-by``,
   ``Signed-off-by``, ``Refs``, …) are kept (engineering_rules §14: single author).
2. **Mandatory, normalized Conventional-Commits scope** — inject this repo's short
   scope when it is missing, and strip the ``qnode-backend-`` / ``qnode-tooling-`` /
   ``qnode-`` prefixes from a repo-name scope. The type is lower-cased and a breaking
   ``!`` is emitted in its canonical position (``type(scope)!: …``).

Usage (from a repo root):
    commit-msg-autofix.py --scope <repo-scope> <commit-msg-file>
"""

from __future__ import annotations

import argparse
import re
import sys

_ROBOT = "\U0001f916"

# Attribution / AI trailer lines (anchored at line start, case-insensitive).
_ATTRIBUTION_LINE = re.compile(
    r"^\s*(?:co-authored-by\s*:"
    r"|co-worked(?:-by|\s+by)\s*:?"
    r"|generated\s+(?:with|by)\b)",
    re.IGNORECASE,
)

# type(scope)!: description  — tolerant of a couple of malformed bang/scope orders.
_HEADER = re.compile(
    r"^(?P<type>[A-Za-z]+)(?P<bang_a>!)?"
    r"(?:\((?P<scope>[^)]*)\))?(?P<bang_b>!)?:[ \t]*(?P<desc>.*)$"
)
# A "(scope):" that leaked into the description (e.g. "feat!:(scope): msg").
_LEADING_SCOPE = re.compile(r"^\((?P<scope>[^)]*)\):[ \t]*(?P<desc>.*)$")


def normalize_scope(scope: str) -> str:
    """Return the short scope: strip the qnode repo-name prefixes if present."""
    s = scope.strip()
    for prefix in ("qnode-backend-", "qnode-tooling-", "qnode-"):
        if s.startswith(prefix):
            return s[len(prefix) :]
    return s


def fix_subject(subject: str, repo_scope: str, strip: bool, log: list[str], force_scope: bool) -> str:
    """Normalize the Conventional-Commits header; return the possibly-rewritten line."""
    m = _HEADER.match(subject)
    if not m:
        log.append("subject is not a Conventional Commit; left for commitlint")
        return subject

    ctype = m.group("type")
    breaking = bool(m.group("bang_a") or m.group("bang_b"))
    scope = m.group("scope")
    desc = m.group("desc")

    if scope is None:  # recover a scope that leaked into the description
        lead = _LEADING_SCOPE.match(desc)
        if lead:
            scope, desc = lead.group("scope"), lead.group("desc")

    new_type = ctype.lower()
    if new_type != ctype:
        log.append(f"lower-cased type: {ctype} -> {new_type}")

    if scope is None or scope.strip() == "":
        new_scope = repo_scope
        log.append(f"added mandatory scope: ({new_scope})")
    else:
        new_scope = normalize_scope(scope) if strip else scope.strip()
        if new_scope != scope:
            log.append(f"normalized scope: ({scope}) -> ({new_scope})")

    bang = "!" if breaking else ""
    if force_scope:
        new_scope = repo_scope
        log.append(f"forced scope: ({scope}) -> ({new_scope})")
    return f"{new_type}({new_scope}){bang}: {desc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", required=True, help="canonical scope for this repo")
    parser.add_argument(
        "--force-scope",
        dest="force_scope",
        action="store_true",
        required=False,
        help="force scope replace"
        )
    parser.add_argument(
        "--no-strip",
        dest="strip",
        action="store_false",
        help="keep an existing scope verbatim (do not strip qnode- prefixes; e.g. qnode-at-home)",
    )
    parser.set_defaults(strip=True)
    parser.set_defaults(force_scope=True)
    parser.add_argument("msgfile", help="path to the commit message file")
    args = parser.parse_args()

    with open(args.msgfile, encoding="utf-8") as fh:
        original = fh.read()
    lines = original.splitlines()
    log: list[str] = []

    # 1. strip attribution / AI trailers (never touch git comment lines).
    kept: list[str] = []
    for line in lines:
        if not line.startswith("#") and (_ATTRIBUTION_LINE.match(line) or _ROBOT in line):
            log.append(f"removed attribution trailer: {line.strip()!r}")
            continue
        kept.append(line)
    lines = kept

    # 2. normalize the subject (first non-blank, non-comment line).
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith("#"):
            lines[i] = fix_subject(line, args.scope, args.strip, log, args.force_scope)
            break

    while lines and lines[-1].strip() == "":  # tidy trailing blanks
        lines.pop()

    new_text = "\n".join(lines) + "\n" if lines else "\n"
    if new_text != original:
        with open(args.msgfile, "w", encoding="utf-8") as fh:
            fh.write(new_text)
    for entry in log:
        print(f"commit-msg autofix: {entry}", file=sys.stderr)
    return 0  # never reject; commitlint validates the result


if __name__ == "__main__":
    raise SystemExit(main())
