# Agentic Development Template

A lightweight Python starting point for working with coding agents. It uses uv for
package management, Ruff for linting and formatting, and pytest for testing.
There are no runtime dependencies; the only direct development dependencies are
Ruff and pytest. No hooks, helper scripts, or containers are required.

## Quick start

Install uv and make sure `uv --version` works, then run these commands from the
repository root:

```sh
uv sync
uv run python -m agentic_development_template
```

The project selects Python 3.12 through `.python-version`. `uv sync` creates the
local `.venv` and installs the package and development tools. You do not need to
activate the environment when using `uv run`.

The sample app prints:

```text
Hello from agentic-development-template!
```

## Project layout

```text
.github/workflows/ci.yml                 GitHub Actions checks
.gitignore                              Excludes environments and caches
.python-version                         Development Python version
AGENTS.md                               Instructions for coding agents
pyproject.toml                          Package metadata and tool configuration
uv.lock                                 Resolved dependency versions
src/agentic_development_template/
    __init__.py                         Sample main() function
    __main__.py                         Entry point for python -m
tests/
    unit/test_main.py                   Imports and calls main()
    e2e/test_smoke.py                   Runs the app in a real subprocess
```

## Everyday commands

Run the full check before considering a change complete:

```sh
uv run ruff check . && uv run ruff format --check . && uv run pytest
```

In shells without `&&` support, run each command separately and stop if one fails.

Apply lint fixes and formatting:

```sh
uv run ruff check --fix .
uv run ruff format .
```

Run only the tests:

```sh
uv run pytest
```

Manage dependencies with uv, never pip or manual dependency-list edits:

```sh
uv add <package>
uv add --dev <package>
```

The template starts without runtime dependencies. Add dependencies only when the
real project needs them, explain why, and commit the resulting `pyproject.toml`
and `uv.lock` changes together.

## Agent workflow and team rules

Read `AGENTS.md` before making changes. It asks agents to propose a plan and wait
for approval for non-trivial work, keep changes focused, test behavior changes,
and run the full check before reporting completion.

Ruff enforces a 100-character line length and checks for common errors, import
ordering, outdated Python patterns, and simplification opportunities. The sample
custom rule bans `os.system` with this guidance:

```text
Use subprocess.run with a list of args.
```

Use the banned-API configuration in `pyproject.toml` to turn repeated review
feedback into checks. The migration exception list starts empty and may only
shrink; do not add exceptions to bypass a failure.

## Continuous integration

GitHub Actions runs on every pull request and push to `main`. It installs uv,
runs `uv sync --locked`, then runs the same lint, formatting, and test checks
shown above. A stale lockfile or failed check fails the job.

## Adapt it for your project

Replace the sample `main()` with your application and extend the tests alongside
it. Keep logic tests under `tests/unit` and subprocess smoke tests under
`tests/e2e`.

Update the description and author metadata in `pyproject.toml`. If you rename
the package, update the directory under `src`, imports, module names in tests
and documentation, and the `[project.scripts]` entry together. Update the project
name in `pyproject.toml`, run `uv sync` to refresh the lockfile, then rerun the
full check and the app.
