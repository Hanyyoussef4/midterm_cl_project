"""
observers.py
============

Observer pattern implementation for side-effects after each calculation.

Classes
-------
Observer :
    Abstract base with a single :meth:`notify` method.
LoggingObserver :
    Logs a one-line summary of every calculation to a rotating file.
AutoSaveObserver :
    Writes the entire history stack to a CSV using *pandas*.

The module is self-contained; concrete observers can be registered with
:py:meth:`app.calculator.Calculator.register_observer`.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

import pandas as pd

from app.calculation import CalculationMemento


# --------------------------------------------------------------------------- #
# Abstract base                                                               #
# --------------------------------------------------------------------------- #

class Observer(ABC):
    """Interface for post-calculation observers."""

    @abstractmethod
    def notify(self, memento: CalculationMemento) -> None:
        """React to a **newly created** memento."""


# --------------------------------------------------------------------------- #
# Concrete observers                                                          #
# --------------------------------------------------------------------------- #

class LoggingObserver(Observer):
    """Append each calculation to a rotating text log.

    Parameters
    ----------
    log_path :
        Path to the log file (will be created if absent).
    """

    def __init__(self, log_path: Path) -> None:
        self._logger = logging.getLogger("CalculatorLogger")
        self._logger.setLevel(logging.INFO)

        # Ensure parent directory exists
        log_path.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def notify(self, memento: CalculationMemento) -> None:  # noqa: D401
        msg = (
            f"{memento.operation_name.upper()} "
            f"{memento.operands[0]}, {memento.operands[1]} = {memento.result}"
        )
        self._logger.info(msg)


class AutoSaveObserver(Observer):
    """Write the entire history to CSV after every calculation."""

    def __init__(self, csv_path: Path, history_provider) -> None:
        """
        Parameters
        ----------
        csv_path :
            Destination CSV file.
        history_provider :
            Callable that returns an iterable of *CalculationMemento* —
            typically ``calculator.history``.
        """
        self._csv_path = csv_path
        self._history_provider = history_provider

        # Ensure directory exists
        csv_path.parent.mkdir(parents=True, exist_ok=True)

    # pandas is imported at top-level; safe in CI.
    def notify(self, _memento: CalculationMemento) -> None:  # noqa: D401
        rows = [m.as_dict() for m in self._history_provider()]
        df = pd.DataFrame(rows)
        df.to_csv(self._csv_path, index=False)


__all__: Sequence[str] = [
    "Observer",
    "LoggingObserver",
    "AutoSaveObserver",
]
