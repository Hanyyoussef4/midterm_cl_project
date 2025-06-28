"""
calculator.py
=============

High-level façade that coordinates:

* Operation resolution (via :class:`app.operations.OperationFactory`)
* Result persistence in :class:`app.history.History`
* Undo / redo functionality
* Observer notifications (logging, auto-save, …)
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from app.calculation import CalculationMemento
from app.history import History
from app.operations import OperationFactory
from app.observers import Observer


class Calculator:
    """User-facing calculator with history, undo/redo, and observers."""

    DEFAULT_MAX_HISTORY = 100

    # ──────────────────────────────────────────────────────────────── #
    # Construction                                                    #
    # ──────────────────────────────────────────────────────────────── #

    def __init__(self, max_history: int | None = None) -> None:
        self._history: History[CalculationMemento] = History(
            max_size=max_history or self.DEFAULT_MAX_HISTORY
        )
        self._observers: List[Observer] = []

    # ──────────────────────────────────────────────────────────────── #
    # Observer management                                             #
    # ──────────────────────────────────────────────────────────────── #

    def register_observer(self, observer: Observer) -> None:
        """Add an observer that will receive every new memento."""
        self._observers.append(observer)

    def unregister_observer(self, observer: Observer) -> None:
        """Remove a previously registered observer (no-op if absent)."""
        try:    # pragma: no cover
            self._observers.remove(observer)    # pragma: no cover
        except ValueError:  # pragma: no cover
            pass  # silent fail is fine for idempotency # pragma: no cover

    def _notify_observers(self, memento: CalculationMemento) -> None:
        """Notify all observers *safely* (one failing observer won’t stop others)."""
        for obs in self._observers:
            try:
                obs.notify(memento)
            except Exception:  # pragma: no cover
                # We deliberately swallow exceptions so one bad observer
                # doesn’t crash the calculator.  In production we might log this.
                pass

    # ──────────────────────────────────────────────────────────────── #
    # Core API                                                        #
    # ──────────────────────────────────────────────────────────────── #

    def evaluate(self, op_name: str, *operands: float) -> float:
        op_obj = OperationFactory.create(op_name, *operands)
        result = op_obj.evaluate()

        memento = CalculationMemento.from_operation(op_obj)
        self._history.push(memento)
        self._notify_observers(memento)
        return result

    # ──────────────────────────────────────────────────────────────── #
    # History helpers (unchanged)                                     #
    # ──────────────────────────────────────────────────────────────── #

    def undo(self) -> CalculationMemento:
        return self._history.undo()

    def redo(self) -> CalculationMemento:
        return self._history.redo()

    def clear_history(self) -> None:
        self._history.clear()

    def history(self) -> Tuple[CalculationMemento, ...]:
        past, _ = self._history.snapshot()
        return tuple(past)

    # ──────────────────────────────────────────────────────────────── #
    # Convenience                                                     #
    # ──────────────────────────────────────────────────────────────── #

    def __len__(self) -> int:  # pragma: no cover
        return len(self._history)


__all__: Sequence[str] = ["Calculator"]
