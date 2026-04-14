from pathlib import Path


def test_score_script_exists() -> None:
    assert Path("scripts/score_agent_probe.py").exists()