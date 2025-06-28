"""
calculator_repl.py
==================

Command-line interface (REPL) for the enhanced calculator.

Supported commands
------------------
add, subtract, multiply, divide, power, root, modulus,
intdivide, percent, absdiff      – perform calculations
history     – display past calculations
clear       – clear history
undo        – undo last calculation
redo        – redo last undone calculation
save <file> – save history to CSV
load <file> – load history from CSV (replaces current)
help        – show this help
exit / quit – leave the program gracefully
"""

from __future__ import annotations

import csv
import shlex
import sys
from pathlib import Path
from typing import Callable, Sequence

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:  # pragma: no cover
    # colour is optional; degrade gracefully
    class _NoColor:
        def __getattr__(self, item):  # noqa: D401
            return ""

    Fore = Style = _NoColor()
    def colorama_init(*_a, **_kw):  # type: ignore
        pass


from app.calculator import Calculator
from app.calculation import CalculationMemento
from app.observers import LoggingObserver, AutoSaveObserver


_PROMPT = f"{Fore.GREEN}calc> {Style.RESET_ALL}"
_HELP_TEXT = __doc__.split("Supported commands")[1].strip()


class CalculatorCLI:
    """Thin wrapper around :class:`~app.calculator.Calculator` for REPL use."""

    def __init__(self) -> None:
        self.calc = Calculator()
        # Attach observers (log + autosave to default paths)
        self.calc.register_observer(
            LoggingObserver(Path("logs") / "calculator.log")
        )
        self.calc.register_observer(
            AutoSaveObserver(Path("history") / "history.csv", self.calc.history)
        )
        self._cmd_map: dict[str, Callable[[Sequence[str]], None]] = {
            "undo": self._cmd_undo,
            "redo": self._cmd_redo,
            "history": self._cmd_history,
            "clear": self._cmd_clear,
            "save": self._cmd_save,
            "load": self._cmd_load,
            "help": self._cmd_help,
            "exit": self._cmd_exit,
            "quit": self._cmd_exit,
        }

    # ------------------------------------------------------------------ #
    # Main loop                                                          #
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        """Start the readline loop until user exits."""
        colorama_init(autoreset=True)
        
        banner = (
            f"{Fore.CYAN}\n"
            "╔═════════════════════════════════════════════════╗\n"
            "║           Welcome to the Enhanced CLI!          ║\n"
            "╚═════════════════════════════════════════════════╝\n"
            f"{Style.RESET_ALL}"
            "Type 'help' to list commands – Ctrl-D or 'exit' to quit.\n"
        )
        print(banner)
        try:
            while True:
                try:
                    line = input(_PROMPT)
                except EOFError:
                    print()  # newline after Ctrl-D
                    break
                self._handle_line(line.strip())
        except KeyboardInterrupt:
            print("\nInterrupted by user.")

    # ------------------------------------------------------------------ #
    # Command dispatcher                                                 #
    # ------------------------------------------------------------------ #

    def _handle_line(self, line: str) -> None:
        if not line:
            return
        parts = shlex.split(line.lower())
        cmd, *args = parts

        # built-in commands
        if cmd in self._cmd_map:
            self._cmd_map[cmd](args)
            return

        # calculation commands
        try:
            operands = [float(a) for a in args]
            if len(operands) != 2:
                raise ValueError("need exactly two numeric operands")
            result = self.calc.evaluate(cmd, *operands)
            print(Fore.YELLOW + f"= {result}" + Style.RESET_ALL)
        except Exception as exc:
            print(Fore.RED + f"Error: {exc}" + Style.RESET_ALL)

    # ------------------------------------------------------------------ #
    # Built-in command handlers                                          #
    # ------------------------------------------------------------------ #

    def _cmd_undo(self, _args) -> None:
        try:
            m = self.calc.undo()
            print(Fore.MAGENTA + f"Undid: {self._fmt_memento(m)}" + Style.RESET_ALL)
        except IndexError:
            print("Nothing to undo.")

    def _cmd_redo(self, _args) -> None:
        try:
            m = self.calc.redo()
            print(Fore.MAGENTA + f"Redid: {self._fmt_memento(m)}" + Style.RESET_ALL)
        except IndexError:
            print("Nothing to redo.")

    def _cmd_history(self, _args) -> None:
        if not self.calc.history():
            print("History is empty.")
            return
        for idx, m in enumerate(self.calc.history(), 1):
            print(f"{idx:>3}: {self._fmt_memento(m)}")

    def _cmd_clear(self, _args) -> None:
        self.calc.clear_history()
        print("History cleared.")

    def _cmd_save(self, args) -> None:
        if not args:
            print("Usage: save <file>")
            return
        dest = Path(args[0])
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.calc.history()[0].as_dict()))
            writer.writeheader()
            writer.writerows(m.as_dict() for m in self.calc.history())
        print(f"History saved to {dest}")

    def _cmd_load(self, args) -> None:
        if not args:
            print("Usage: load <file>")
            return
        src = Path(args[0])
        if not src.exists():
            print("File not found.")
            return
        with src.open() as f:
            reader = csv.DictReader(f)
            self.calc.clear_history()
            for row in reader:
                m = CalculationMemento(
                    operation_name=row["operation"].lower(),
                    operands=(float(row["op1"]), float(row["op2"])),
                    result=float(row["result"]),
                    timestamp=row["timestamp"],
                )
                # push directly so observers don't fire
                self.calc._history.push(m)  # type: ignore[attr-defined]
        print(f"History loaded from {src}")

    def _cmd_help(self, _args) -> None:
        print(_HELP_TEXT)

    def _cmd_exit(self, _args) -> None:  # noqa: D401
        print("Goodbye!")
        sys.exit(0)

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _fmt_memento(m: CalculationMemento) -> str:
        return (
            f"{m.timestamp} | {m.operation_name.upper()} "
            f"{m.operands[0]}, {m.operands[1]} = {m.result}"
        )


# --------------------------------------------------------------------------- #
# Entrypoint                                                                  #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    CalculatorCLI().run()
