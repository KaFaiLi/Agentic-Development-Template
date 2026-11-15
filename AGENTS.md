# AGENTS.md

## Commands
- Setup: `uv sync --locked && uv run --locked pre-commit install`
- Verify before completion:
  `uv run --locked pre-commit run --all-files && uv run --locked pytest`
- Run: `uv run --locked python -m agentic_development_template`
- Dependencies: `uv add <pkg>` or `uv add --dev <pkg>`.
  Explain why first; never use pip or edit dependency lists manually.

Review any automatic fixes and rerun verification until it passes.
Do not bypass failing hooks.

## Workflow
1. Plan first for any non-trivial change (touches more than 2 files, adds behavior,
   refactors, or migrates). Present: goal, files to change, tests to add, risks.
   Wait for approval before writing code. Small, obvious fixes can skip this.
2. Implement in small steps. Keep changes focused.
3. Verify: run the check command. Report the actual results, including failures.

## Review expectations
- Use domain-specific names: snake_case for functions/variables, PascalCase for
  classes, and UPPER_SNAKE_CASE for constants. Do not shadow Python built-ins.
- Reuse existing helpers; avoid abstractions or configuration for hypothetical needs.
- Test observable behavior and failure cases, not implementation details.
- Remove debugging calls and obsolete lint suppressions. Any necessary suppression
  must name the specific rule and explain why; never use it just to pass checks.

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

## Parallel work
- One session per git worktree: `git worktree add ../wt-<name> -b <name>`
- Clean up after merge: `git worktree remove ../wt-<name>`
