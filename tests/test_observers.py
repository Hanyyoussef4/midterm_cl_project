"""
test_observers.py
=================

Validates that `LoggingObserver` and `AutoSaveObserver` are correctly
invoked by :class:`app.calculator.Calculator`.

Each test uses *tmp_path* to ensure the filesystem side-effects are
isolated and automatically cleaned up.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd
import pytest

from app.calculator import Calculator
from app.observers import AutoSaveObserver, LoggingObserver


# --------------------------------------------------------------------------- #
# Helper                                                                      #
# --------------------------------------------------------------------------- #

def _setup_calc(tmp_path: Path):
    """Return a calculator wired with both observers and ready for testing."""
    calc = Calculator(max_history=None)

    log_file = tmp_path / "calc.log"
    csv_file = tmp_path / "history.csv"

    calc.register_observer(LoggingObserver(log_file))
    calc.register_observer(AutoSaveObserver(csv_file, calc.history))
    return calc, log_file, csv_file


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_logging_observer_writes_line(tmp_path: Path) -> None:
    """Ensure each evaluation appends a human-readable line to the log file."""
    calc, log_file, _ = _setup_calc(tmp_path)

    calc.evaluate("add", 2, 3)   # 2 + 3 = 5
    calc.evaluate("multiply", 2, 4)  # 2 × 4 = 8

    contents = log_file.read_text(encoding="utf-8")
    assert "ADD 2, 3 = 5" in contents
    assert "MULTIPLY 2, 4 = 8" in contents


def test_autosave_observer_writes_csv(tmp_path: Path) -> None:
    """CSV file is overwritten after each calculation with full history."""
    calc, _log_file, csv_file = _setup_calc(tmp_path)

    calc.evaluate("power", 2, 3)   # 8
    calc.evaluate("subtract", 10, 4)  # 6

    # pandas reads our CSV back
    df = pd.read_csv(csv_file)
    assert len(df) == 2
    assert list(df["result"]) == [8, 6]


def test_observer_error_does_not_break_evaluate(tmp_path: Path) -> None:
    """A failing observer should not crash the Calculator."""

    class BadObserver:
        def notify(self, _memento):  # noqa: D401
            raise RuntimeError("observer blew up")

    calc, _log_file, _csv_file = _setup_calc(tmp_path)
    calc.register_observer(BadObserver())  # intentionally bad

    # evaluate returns correct result despite observer failure
    assert calc.evaluate("intdivide", 9, 4) == 2

