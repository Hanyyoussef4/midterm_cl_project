"""
test_observer_errors.py
=======================

Validate that observers are **not** notified when an evaluation raises
(e.g. divide by zero).
"""

from __future__ import annotations

from app.calculator import Calculator


def test_observers_not_called_on_error() -> None:
    calc = Calculator()
    called = False

    class SpyObserver:
        def notify(self, _memento):  # noqa: D401
            nonlocal called
            called = True

    calc.register_observer(SpyObserver())

    # Trigger a division-by-zero ValueError
    try:
        calc.evaluate("divide", 5, 0)
    except ValueError:
        pass

    assert called is False, "Observer should not fire on failed evaluation"
