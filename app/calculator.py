"""
calculator.py
=============

High-level façade that coordinates:

* Operation resolution (via :class:`app.operations.OperationFactory`)
* Result persistence (creates a :class:`app.calculation.CalculationMemento`
  and stores it in :class:`app.history.History`)
* Undo / redo functionality
"""

from __future__ import annotations

from typing import Sequence, Tuple

from app.calculation import CalculationMemento
from app.history import History
from app.operations import OperationFactory


class Calculator:
    """User-facing calculator with history and undo/redo support."""

    #: Maximum number of mementos to retain (``None`` → unlimited)
    DEFAULT_MAX_HISTORY = 100

    # ------------------------------------------------------------------ #
    # Construction                                                       #
    # ------------------------------------------------------------------ #

    def __init__(self, max_history: int | None = None) -> None:
        self._history: History[CalculationMemento] = History(
            max_size=max_history or self.DEFAULT_MAX_HISTORY
        )

    # ------------------------------------------------------------------ #
    # Core API                                                           #
    # ------------------------------------------------------------------ #

    def evaluate(self, op_name: str, *operands: float) -> float:
        """Evaluate *op_name* with *operands* and record the result.

        Parameters
        ----------
        op_name :
            Keyword such as ``"add"`` or ``"percent"`` (case-insensitive).
        operands :
            Two numeric values.

        Returns
        -------
        float
            The operation result.

        Raises
        ------
        ValueError
            If the operation keyword is unknown or the math is invalid.
        """
        op_obj = OperationFactory.create(op_name, *operands)
        result = op_obj.evaluate()

        # snapshot for history
        self._history.push(CalculationMemento.from_operation(op_obj))
        return result

    # ------------------------------------------------------------------ #
    # History helpers                                                    #
    # ------------------------------------------------------------------ #

    def undo(self) -> CalculationMemento:
        """Undo the last calculation and return its memento.

        Raises
        ------
        IndexError
            If the history is empty.
        """
        return self._history.undo()

    def redo(self) -> CalculationMemento:
        """Redo the last undone calculation and return its memento."""
        return self._history.redo()

    def clear_history(self) -> None:
        """Erase all stored mementos."""
        self._history.clear()

    def history(self) -> Tuple[CalculationMemento, ...]:
        """Return a **copy** of the current history stack (oldest → newest)."""
        past, _future = self._history.snapshot()
        return tuple(past)

    # ------------------------------------------------------------------ #
    # Convenience                                                        #
    # ------------------------------------------------------------------ #

    def __len__(self) -> int:  # pragma: no cover
        return len(self._history)


__all__: Sequence[str] = ["Calculator"]
