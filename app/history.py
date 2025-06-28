"""
History stack for calculator mementos.

Implements:

    • push(memento)
    • undo()  -> memento
    • redo()  -> memento
    • clear()
    • __len__ and __bool__

Design: two deques (“past” and “future”) give O(1) push/undo/redo.
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Generic, Iterable, TypeVar

T = TypeVar("T")


class History(Generic[T]):
    """Undo/redo stack using two internal deques."""

    def __init__(self, max_size: int | None = None) -> None:
        # Older items on the *left*, newest on the *right*.
        self._past: Deque[T] = deque(maxlen=max_size)
        self._future: Deque[T] = deque(maxlen=max_size)

    # ────────────────────────────────────────────────────────────
    # Core API
    # ────────────────────────────────────────────────────────────

    def push(self, item: T) -> None:
        """Record a new memento and clear the redo stack."""
        self._past.append(item)
        self._future.clear()

    def undo(self) -> T:
        """Pop the most-recent item and move it to the redo stack."""
        if not self._past:
            raise IndexError("nothing to undo")
        item = self._past.pop()
        self._future.append(item)
        return item

    def redo(self) -> T:
        """Re-apply the last undone item."""
        if not self._future:
            raise IndexError("nothing to redo")
        item = self._future.pop()
        self._past.append(item)
        return item

    def clear(self) -> None:
        """Erase both stacks."""
        self._past.clear()
        self._future.clear()

    # ────────────────────────────────────────────────────────────
    # Dunder helpers
    # ────────────────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._past)

    def __bool__(self) -> bool:  # pragma: no cover
        return bool(self._past)

    # Convenience for debugging/tests
    def snapshot(self) -> tuple[Iterable[T], Iterable[T]]:  # pragma: no cover
        """Return (past, future) as two immutable tuples."""
        return tuple(self._past), tuple(self._future)
