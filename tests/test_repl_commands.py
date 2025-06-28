"""
test_repl_commands.py
=====================

Drive CalculatorCLI internals directly so calculator_repl.py receives
coverage without interactive input.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from app.calculator_repl import CalculatorCLI


def _new_cli(tmp_path: Path) -> CalculatorCLI:
    """Create CLI with observers disabled (to avoid file writes)."""
    cli = CalculatorCLI()
    cli.calc._observers.clear()          # type: ignore[attr-defined]
    cli._cmd_save = lambda *_a, **_kw: None  # type: ignore[attr-defined]
    cli._cmd_load = lambda *_a, **_kw: None  # type: ignore[attr-defined]
    return cli


def test_basic_calculations_and_history(capsys, tmp_path):
    cli = _new_cli(tmp_path)

    cli._handle_line("add 2 3")
    cli._handle_line("power 2 5")
    cli._handle_line("history")

    out = capsys.readouterr().out
    assert "= 5" in out and "= 32" in out
    assert "ADD" in out and "POWER" in out


@pytest.mark.parametrize("cmd", ["undo", "redo", "clear", "help"])
def test_single_word_commands(cmd, capsys, tmp_path):
    cli = _new_cli(tmp_path)
    cli._handle_line(cmd)
    out = capsys.readouterr().out
    # A simple sanity check that the command produced some output
    assert out.strip() != ""


def test_friendly_error_message(capsys, tmp_path):
    cli = _new_cli(tmp_path)
    cli._handle_line("divide 5 0")
    out = capsys.readouterr().out
    assert "dividing by zero is not allowed" in out.lower()
