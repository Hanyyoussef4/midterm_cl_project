"""
calculation.py
==============

Defines :class:`CalculationMemento`, an **immutable** snapshot of a single
calculator evaluation.  A memento records the operation name, the pair of
operands, the numeric result, and a UTC timestamp.  The class is dataclass-
based, slot-optimised, and provides helpers for logging / CSV export.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Sequence, Tuple


@dataclass(frozen=True, slots=True)
class CalculationMemento:
    """Immutable record of one calculation.

    Attributes
    ----------
    operation_name :
        Lower-case keyword that identifies the operation (e.g. ``"add"``).
    operands :
        Tuple of two floats in the order supplied by the user.
    result :
        The numeric outcome of the calculation.
    timestamp :
        ISO-8601 UTC time when the memento was created.
    """

    operation_name: str
    operands: Tuple[float, float]
    result: float
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds")
    )

    # --------------------------------------------------------------------- #
    # Public helpers                                                         #
    # --------------------------------------------------------------------- #

    def as_dict(self) -> dict[str, str | float]:
        """Return the memento as a flat dict ready for CSV / JSON logging."""
        return {
            "timestamp": self.timestamp,
            "operation": self.operation_name,
            "op1": self.operands[0],
            "op2": self.operands[1],
            "result": self.result,
        }

    # Factory constructor -------------------------------------------------- #

    @classmethod
    def from_operation(cls, op_obj) -> "CalculationMemento":  # type: ignore
        """Create a memento directly from an *Operation* instance."""
        return cls(
            operation_name=op_obj.name,
            operands=op_obj.operands,      # type: ignore[arg-type]
            result=op_obj.evaluate(),
        )


__all__: Sequence[str] = ["CalculationMemento"]
