"""
test_history.py
===============

End-to-end tests for the *history stack* living inside :class:`app.calculator.Calculator`.

Scenarios covered
-----------------
* Normal push / undo / redo flow.
* Multiple undos / redos in sequence.
* Edge-cases: undo / redo on empty stack, clear_history().
"""

from __future__ import annotations

import math
import pytest

from app.calculator import Calculator
from app.calculation import CalculationMemento


def _new_calc() -> Calculator:
    """Utility: create a calculator with unlimited history for the tests."""
    return Calculator(max_history=None)


# --------------------------------------------------------------------------- #
# Happy-path                                                                   #
# --------------------------------------------------------------------------- #

def test_push_and_undo_redo() -> None:
    calc = _new_calc()

    # push two operations
    assert math.isclose(calc.evaluate("add", 2, 3), 5)
    assert math.isclose(calc.evaluate("multiply", 4, 2), 8)
    assert len(calc) == 2

    # undo last op
    last = calc.undo()
    assert isinstance(last, CalculationMemento)
    assert last.result == 8
    assert len(calc) == 1

    # redo brings it back
    redone = calc.redo()
    assert redone.result == 8
    assert len(calc) == 2


# --------------------------------------------------------------------------- #
# Multi-step undo / redo                                                      #
# --------------------------------------------------------------------------- #

def test_multi_level_undo_redo() -> None:
    calc = _new_calc()
    results = [calc.evaluate("add", i, i) for i in range(3)]  # 0+0, 1+1, 2+2
    assert results == [0, 2, 4]
    assert len(calc) == 3

    a = calc.undo()           # pop 2+2
    b = calc.undo()           # pop 1+1
    assert (a.result, b.result) == (4, 2)
    assert len(calc) == 1

    # redo twice restores both
    calc.redo()
    calc.redo()
    assert len(calc) == 3
    # latest result back on top
    assert calc.history()[-1].result == 4


# --------------------------------------------------------------------------- #
# Edge cases                                                                   #
# --------------------------------------------------------------------------- #

def test_undo_redo_empty_stack() -> None:
    calc = _new_calc()

    with pytest.raises(IndexError):
        calc.undo()

    # After one calculate + undo, redo is allowed once, then fails.
    calc.evaluate("power", 2, 3)
    calc.undo()
    calc.redo()
    with pytest.raises(IndexError):
        calc.redo()


def test_clear_history() -> None:
    calc = _new_calc()
    calc.evaluate("add", 1, 1)
    calc.evaluate("subtract", 10, 4)

    calc.clear_history()
    assert len(calc) == 0

    with pytest.raises(IndexError):
        calc.undo()
