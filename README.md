# 🚀 Enhanced Calculator CLI

[![CI Status](https://github.com/HanyYoussef4/midterm_cl_project/actions/workflows/python-app.yml/badge.svg)](https://github.com/HanyYoussef4/midterm_cl_project/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/HanyYoussef4/midterm_cl_project/actions)

> **Midterm Project – Advanced Command-Line Calculator**
> Demonstrates Python design patterns, REPL development, undo/redo, observer logging, CSV I/O, and 100 % test coverage.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features & Patterns](#features--patterns)
3. [Folder Structure](#folder-structure)
4. [Installation](#installation)
5. [Configuration & Logging](#configuration--logging)
6. [Using the CLI](#using-the-cli)
7. [Testing Instructions](#testing-instructions)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [Extending the Calculator](#extending-the-calculator)
10. [License](#license)

---

## Project Overview

A **fully-featured CLI calculator** that meets midterm requirements while following professional Python practices:

* **Factory Pattern** for dynamically instantiating 11 arithmetic operations
* **Memento Pattern** for undo/redo via history stack
* **Observer Pattern** for logging and auto-saving
* A colorized **REPL** with commands: `help`, `history`, `undo`, `redo`, `save`, `load`, *etc.*
* **100 % unit-test coverage** enforced by CI

---

## Features & Patterns

| Layer      | Key Classes                           | Pattern      | Responsibility                             |
| ---------- | ------------------------------------- | ------------ | ------------------------------------------ |
| Operations | `Operation` ABC, `Add`, …             | **Factory**  | Validate inputs & perform arithmetic       |
| History    | `History`, `CalculationMemento`       | **Memento**  | Record, undo, redo past calculations       |
| Observers  | `LoggingObserver`, `AutoSaveObserver` | **Observer** | React to each new calculation (log & save) |
| CLI        | `CalculatorREPL`, `main.py`           | –            | Parse commands, dispatch ops, handle I/O   |

---

## Folder Structure

```
midterm_cl_project/
│  .coveragerc               # Coverage rules
│  .env.example              # Config template (rename to .env)
│  README.md                 # ← you are here
│  requirements.txt          # Dependencies
│  .github/
│  └─ workflows/
│     └─ python-app.yml      # CI pipeline
│
├─ app/                      # Application package
│  ├─ operations.py          # 11 ops + Factory
│  ├─ history.py             # Undo/redo stack
│  ├─ calculation.py         # Memento dataclass
│  ├─ observers.py           # Observer implementations
│  ├─ calculator.py          # Core façade (history + observers)
│  ├─ calculator_repl.py     # Interactive REPL logic
│  └─ __init__.py
│
├─ history/                  # Default CSV auto-save folder
│  └─ history.csv
│
├─ logs/                     # Logging output
│  └─ calculator.log
│
└─ tests/                    # 47 pytest cases (100 % coverage)
   ├─ test_operations.py
   ├─ test_history.py
   ├─ test_observers.py
   ├─ test_cli_save_load.py
   └─ test_repl_commands.py
```

---

## Installation

### macOS / Linux

```bash
# Clone repository
git clone https://github.com/HanyYoussef4/midterm_cl_project.git
cd midterm_cl_project

# Create & activate virtual environment (Python 3.9+)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy and edit config
cp .env.example .env
```

### Windows (PowerShell)

```powershell
git clone https://github.com/HanyYoussef4/midterm_cl_project.git
cd midterm_cl_project

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

copy .env.example .env
```

---

## Configuration & Logging

All settings live in your `.env` (created from `.env.example`):

```ini
CALCULATOR_LOG_DIR=logs                     # Where calculator.log is written
CALCULATOR_HISTORY_DIR=history              # Folder for autosave CSV
HISTORY_FILE=history/history.csv            # Default file for manual & auto save
CALCULATOR_MAX_HISTORY_SIZE=100             # Max undo/redo entries
CALCULATOR_AUTO_SAVE=true                   # Toggle autosave observer
```

* **Logging:**
  Logs are written to `logs/calculator.log` via `LoggingObserver`.
  Level and format in `app/logger.py`.

* **History autosave:**
  After each calculation, `AutoSaveObserver` writes last N entries (≤ `CALCULATOR_MAX_HISTORY_SIZE`) to `HISTORY_FILE`.

---

## Using the CLI

Launch via either:

```bash
python main.py
# or
python -m app.calculator_repl
```

You’ll see:

```
╔════════════════════════════════════════╗
║       Welcome to the Enhanced CLI!     ║
╚════════════════════════════════════════╝
Type 'help' for commands – Ctrl-D or 'exit' to quit.

calc>
```

Example session:

```text
calc> add 2 3
= 5
calc> power 2 5
= 32
calc> history
  1: ADD 2,3 = 5
  2: POWER 2,5 = 32

# Manual save overwrites default file
calc> save
Saved 2 entries to history/history.csv

# Load default
calc> load
Loaded 2 entries from history/history.csv

# Undo/redo
calc> undo
calc> redo

calc> exit
Goodbye!
```

---

## Testing Instructions

```bash
pytest --cov app --cov-config=.coveragerc --cov-report term-missing
```

* **47 tests** covering all operations, history, observers, CLI, save/load, REPL
* **100 % line & branch coverage**
* CI enforces a 90 % coverage gate

---

## CI/CD Pipeline

Defined in `.github/workflows/python-app.yml`:

1. Checkout & setup Python (3.9+)
2. Install dependencies
3. Run `pytest` with coverage
4. Fail if coverage < 90 %

Badges at the top update on every push.

---

## Extending the Calculator

* **Add operations**: subclass `Operation` and register in the factory
* **Adjust history**: change `CALCULATOR_MAX_HISTORY_SIZE` in `.env`
* **Toggle autosave**: set `CALCULATOR_AUTO_SAVE=false`
* **Package CLI**: add `console_scripts` in `setup.py` or `pyproject.toml`

Contributions welcome—maintain ≥ 90 % coverage.

---
