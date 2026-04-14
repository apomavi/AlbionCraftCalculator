from pathlib import Path


def test_probe_script_exists() -> None:
    assert Path("scripts/probe_agents.py").exists()