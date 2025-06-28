"""
Operations module
=================

Defines a common `Operation` interface plus concrete implementations for all
mandatory arithmetic functions:

    add, subtract, multiply, divide, power, root, modulus, int_divide,
    percent, abs_diff

Each concrete class is generated dynamically to avoid boilerplate.  A
convenient `OperationFactory` converts an operation keyword (e.g. ``"add"``)
and operands into the correct `Operation` instance.

All operations expect **exactly two operands**; validation is performed in the
base class.  Mathematical error cases (e.g. divide-by-zero) raise
``ValueError``.
"""

from __future__ import annotations

from abc import ABC
from typing import Callable, Sequence


# --------------------------------------------------------------------------- #
# Base class                                                                  #
# --------------------------------------------------------------------------- #

class Operation(ABC):
    """Abstract base class for a calculator operation."""

    # These attributes are injected when the concrete subclasses are created.
    name: str                      # short keyword, lowercase
    num_args: int                  # how many operands are required
    func: Callable[..., float]     # pure function that performs the math

    def __init__(self, *operands: float) -> None:
        if len(operands) != self.num_args:
            raise ValueError(
                f"{self.name} expects {self.num_args} arguments, "
                f"got {len(operands)}"
            )
        self.operands: tuple[float, ...] = tuple(operands)

    # ------------------------------------------------------------------ #
    # Public API                                                          #
    # ------------------------------------------------------------------ #

    def evaluate(self) -> float:
        """Compute and return the numeric result."""
        return self.func(*self.operands)

    # ------------------------------------------------------------------ #
    # Representation helpers                                              #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}{self.operands}"

    def __str__(self) -> str:  # pragma: no cover
        joined = ", ".join(str(x) for x in self.operands)
        return f"{self.name}({joined}) = {self.evaluate()}"


# --------------------------------------------------------------------------- #
# Helper lambdas & error helper                                               #
# --------------------------------------------------------------------------- #

def _err(msg: str) -> None:  # pragma: no cover
    raise ValueError(msg)


_add      = lambda a, b: a + b
_sub      = lambda a, b: a - b
_mul      = lambda a, b: a * b
_div      = lambda a, b: a / b if b != 0 else _err("division by zero")
_pow      = lambda a, b: a ** b
_root     = lambda a, n: a ** (1 / n) if n != 0 else _err("zero root")
_mod      = lambda a, b: a % b if b != 0 else _err("modulo by zero")
_intdiv   = lambda a, b: a // b if b != 0 else _err("int divide by zero")
_percent  = lambda a, b: (a / b) * 100 if b != 0 else _err("percent div by zero")
_absdiff  = lambda a, b: abs(a - b)


# --------------------------------------------------------------------------- #
# Dynamic subclass factory (eliminates boilerplate)                           #
# --------------------------------------------------------------------------- #

def _make_op(name: str, fn: Callable[..., float]) -> type[Operation]:
    """Return a new Operation subclass bound to *fn* with two operands."""
    return type(
        name,
        (Operation,),
        {
            "name": name.lower(),
            "num_args": 2,
            "func": staticmethod(fn),
        },
    )


# Concrete operation classes
Add        = _make_op("Add", _add)
Subtract   = _make_op("Subtract", _sub)
Multiply   = _make_op("Multiply", _mul)
Divide     = _make_op("Divide", _div)
Power      = _make_op("Power", _pow)
Root       = _make_op("Root", _root)
Modulus    = _make_op("Modulus", _mod)
IntDivide  = _make_op("IntDivide", _intdiv)
Percent    = _make_op("Percent", _percent)
AbsDiff    = _make_op("AbsDiff", _absdiff)


# --------------------------------------------------------------------------- #
# Operation factory                                                           #
# --------------------------------------------------------------------------- #

class OperationFactory:
    """Create an Operation instance from a keyword and operand list."""

    _registry: dict[str, type[Operation]] = {
        cls.name: cls
        for cls in (
            Add, Subtract, Multiply, Divide, Power, Root,
            Modulus, IntDivide, Percent, AbsDiff,
        )
    }

    @classmethod
    def create(cls, op_name: str, *operands: float) -> Operation:
        try:
            op_cls = cls._registry[op_name.lower()]
        except KeyError as exc:
            valid = ", ".join(sorted(cls._registry))
            raise ValueError(
                f"Unknown operation '{op_name}'. Valid options: {valid}"
            ) from exc
        return op_cls(*operands)


# --------------------------------------------------------------------------- #
# Public re-exports                                                           #
# --------------------------------------------------------------------------- #

__all__: Sequence[str] = [
    "Operation",
    "Add", "Subtract", "Multiply", "Divide",
    "Power", "Root", "Modulus", "IntDivide", "Percent", "AbsDiff",
    "OperationFactory",
]
