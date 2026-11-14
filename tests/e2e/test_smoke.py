import subprocess
import sys


def test_app_runs():
    r = subprocess.run(
        [sys.executable, "-m", "agentic_development_template"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0
    assert r.stdout.strip()
