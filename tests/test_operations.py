
"""
Parametrised tests for every concrete Operation class and the OperationFactory.
"""

from __future__ import annotations

import math
import pytest

import app.operations as ops


# -------------------------------------------------------------------- #
# Happy-path evaluation                                                 #
# -------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "op_cls, operands, expected",
    [
        (ops.Add,        (5, 7),     12),
        (ops.Subtract,   (10, 4),    6),
        (ops.Multiply,   (3, 4),     12),
        (ops.Divide,     (9, 3),     3),
        (ops.Power,      (2, 3),     8),
        (ops.Root,       (27, 3),    3),
        (ops.Modulus,    (10, 4),    2),
        (ops.IntDivide,  (10, 4),    2),
        (ops.Percent,    (25, 200),  12.5),
        (ops.AbsDiff,    (10, 3),    7),
    ],
)
def test_operation_evaluate(op_cls, operands, expected) -> None:
    op = op_cls(*operands)
    assert math.isclose(op.evaluate(), expected, rel_tol=1e-9)


# -------------------------------------------------------------------- #
# Argument-count validation                                             #
# -------------------------------------------------------------------- #

@pytest.mark.parametrize("op_cls", [
    ops.Add, ops.Subtract, ops.Multiply, ops.Divide, ops.Power, ops.Root,
    ops.Modulus, ops.IntDivide, ops.Percent, ops.AbsDiff,
])
def test_wrong_arity(op_cls) -> None:
    with pytest.raises(ValueError):
        op_cls(1)              # too few
    with pytest.raises(ValueError):
        op_cls(1, 2, 3)        # too many


# -------------------------------------------------------------------- #
# Error cases (÷0 etc.)                                                 #
# -------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "op_cls, operands",
    [
        (ops.Divide,    (5, 0)),
        (ops.Modulus,   (5, 0)),
        (ops.IntDivide, (5, 0)),
        (ops.Percent,   (5, 0)),
        (ops.Root,      (8, 0)),
    ],
)
def test_invalid_math(op_cls, operands) -> None:
    with pytest.raises(ValueError):
        op_cls(*operands).evaluate()


# -------------------------------------------------------------------- #
# Factory                                                               #
# -------------------------------------------------------------------- #

def test_factory_valid() -> None:
    op = ops.OperationFactory.create("add", 2, 3)
    assert isinstance(op, ops.Add)
    assert op.evaluate() == 5


def test_factory_invalid() -> None:
    with pytest.raises(ValueError):
        ops.OperationFactory.create("nonexistent", 1, 2)

# -------------------------------------------------------------------- #
# Error-handling: divide / modulo / root by zero                       #
# -------------------------------------------------------------------- #

from app.operations import OperationFactory

@pytest.mark.parametrize(
    "op_name, a, b",
    [
        ("divide",    5, 0),
        ("modulus",   5, 0),
        ("intdivide", 5, 0),
        ("percent",   5, 0),
        ("root",      8, 0),
    ],
)
def test_zero_division_family(op_name, a, b) -> None:
    """Every op that relies on a non-zero denominator should raise."""
    with pytest.raises(ValueError):
        OperationFactory.create(op_name, a, b).evaluate()
