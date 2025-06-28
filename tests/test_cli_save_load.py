"""
test_cli_save_load.py
=====================

Ensures the REPL's internal save/load helpers write a CSV correctly and
reload it into a new session without data loss.
"""

from __future__ import annotations

from pathlib import Path

from app.calculator_repl import CalculatorCLI


def test_save_then_load_history(tmp_path: Path) -> None:
    """Round-trip: evaluate ➜ save ➜ load ➜ history identical."""
    # First CLI instance — create some history
    cli1 = CalculatorCLI()
    cli1.calc.evaluate("add", 2, 3)     # result = 5
    cli1.calc.evaluate("multiply", 4, 2)  # result = 8
    assert len(cli1.calc.history()) == 2

    # Save to temp CSV using the private helper (avoids interactive input)
    csv_path = tmp_path / "history.csv"
    cli1._cmd_save([str(csv_path)])  # type: ignore[attr-defined]
    assert csv_path.exists() and csv_path.stat().st_size > 0

    # New CLI instance — load the CSV
    cli2 = CalculatorCLI()
    cli2._cmd_load([str(csv_path)])  # type: ignore[attr-defined]
    hist = cli2.calc.history()

    # Validate history integrity
    assert len(hist) == 2
    assert hist[0].result == 5
    assert hist[1].result == 8
