# AGENTS.md

## Commands
- Install: `uv sync --locked`, then `uv run --locked pre-commit install` in each checkout.
- Check (run before reporting any task as done):
  `uv run --locked ruff check . && uv run --locked ruff format --check . && uv run --locked pytest`
- Auto-fix: `uv run --locked ruff check --fix . && uv run --locked ruff format .`
- Hooks: `uv run --locked pre-commit run --all-files`.
  Hooks fix lint and formatting on staged Python files using the locked Ruff version.
  Inspect automatic changes, stage them, and retry the commit. Do not bypass hooks
  merely to make a commit succeed. Hooks supplement the full check; CI stays check-only.
- Run the app: `uv run python -m agentic_development_template`
- Add dependencies: `uv add <pkg>` (runtime) or `uv add --dev <pkg>` (dev).
  Never use pip or edit dependency lists by hand. Say why before adding any dependency.

## Workflow
1. Plan first for any non-trivial change (touches more than 2 files, adds behavior,
   refactors, or migrates). Present: goal, files to change, tests to add, risks.
   Wait for approval before writing code. Small, obvious fixes can skip this.
2. Implement in small steps. Keep changes focused; do not refactor unrelated code.
3. Verify: run the check command. Never say "done" while it fails.
   Report the actual results, including failures.

## Testing
- tests/unit: logic tests. tests/e2e: run the real app in a subprocess.
- Every behavior change needs a test. For a bug fix, write the failing test first.
- For user-facing behavior, confirm it by running the app, not only unit tests.

## Lint rules from repeated review feedback
- If the same review comment comes up about 3 times, or a reviewer says
  "always" or "never", propose a lint rule instead of fixing it by hand again.
- Prefer, in order:
  1. A built-in Ruff rule added to `select` in pyproject.toml.
  2. `banned-api` (TID251) with a message saying what to use instead.
  3. If the pattern is structural (not a name or import), tell me and ask before
     adding any new tool.
- When adding a rule: put it in pyproject.toml, fix existing violations, run the
  check command. Do not silence a failure with `# noqa` just to pass; fix it or ask.

## Migrations
- Never mix old and new patterns. New code uses the new pattern only.
- Files still on the old pattern are listed in `per-file-ignores` in pyproject.toml.
  That list may only shrink. Never add a file to it.
- When you touch a legacy file, migrate it and remove its entry.
- Do not copy patterns from legacy files into new code.
- PR CI compares both Ruff per-file exception tables against the PR base and rejects
  added patterns or broader rule exemptions. Reproduce on committed changes with
  `uv run --locked python scripts/check_migration_exceptions.py --base-ref origin/main`.
  This guard does not enforce other Ruff settings or detect new inline `noqa` comments.

## Safety
- Do not read or modify .env files or secrets.
- Ask before: force-pushing, deleting files recursively, or running commands that
  execute arbitrary code (`find -exec`, bulk `sed -i`, `curl | sh`).

## Parallel work
- One session per git worktree: `git worktree add ../wt-<name> -b <name>`
- Clean up after merge: `git worktree remove ../wt-<name>`
