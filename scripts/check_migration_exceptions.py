"""Reject added or broadened Ruff per-file exceptions between two Git revisions."""

import argparse
import subprocess
import sys
import tomllib


def read_exceptions(ref: str) -> dict[str, set[str]]:
    result = subprocess.run(
        ["git", "show", f"{ref}:pyproject.toml"],
        check=True,
        capture_output=True,
        text=True,
    )
    lint = tomllib.loads(result.stdout).get("tool", {}).get("ruff", {}).get("lint", {})
    exceptions: dict[str, set[str]] = {}
    for table in ("per-file-ignores", "extend-per-file-ignores"):
        for pattern, rules in lint.get(table, {}).items():
            exceptions.setdefault(pattern, set()).update(rules)
    return exceptions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", required=True, help="Existing comparison revision")
    parser.add_argument("--head-ref", default="HEAD", help="Candidate revision (default: HEAD)")
    args = parser.parse_args()
    try:
        base = read_exceptions(args.base_ref)
        head = read_exceptions(args.head_ref)
    except (subprocess.CalledProcessError, tomllib.TOMLDecodeError) as exc:
        print(f"Cannot compare migration exceptions: {exc}", file=sys.stderr)
        return 1

    added = [
        (pattern, rule)
        for pattern, rules in head.items()
        for rule in rules
        if not any(
            previous == "ALL" or (rule != "ALL" and rule.startswith(previous))
            for previous in base.get(pattern, set())
        )
    ]
    if added:
        for pattern, rule in sorted(added):
            print(f"Added or broadened migration exception: {pattern}: {rule}", file=sys.stderr)
        return 1
    print("Migration exceptions did not grow.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
