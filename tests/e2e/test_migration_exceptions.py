import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_migration_exceptions.py"


@pytest.mark.parametrize("table", ["per-file-ignores", "extend-per-file-ignores"])
@pytest.mark.parametrize(
    ("base", "head", "expected"),
    [
        ('"legacy.py" = ["TID251"]', '"legacy.py" = ["TID251"]', 0),
        ('"legacy.py" = ["TID251"]', "", 0),
        ('"legacy.py" = ["TID"]', '"legacy.py" = ["TID251"]', 0),
        ("", '"new.py" = ["TID251"]', 1),
        ('"legacy.py" = ["TID251"]', '"legacy.py" = ["TID"]', 1),
        ('"legacy.py" = ["TID251"]', '"*.py" = ["TID251"]', 1),
    ],
)
def test_exception_ratchet(tmp_path, table, base, head, expected):
    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True
        )

    def commit(rules):
        (tmp_path / "pyproject.toml").write_text(
            f"[tool.ruff.lint.{table}]\n{rules}\n", encoding="utf-8"
        )
        git("add", "pyproject.toml")
        git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "test")

    git("init")
    commit(base)
    base_ref = git("rev-parse", "HEAD").stdout.strip()
    if base != head:
        commit(head)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--base-ref", base_ref],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == expected, result.stdout + result.stderr
    if expected:
        assert "Added or broadened migration exception" in result.stderr
