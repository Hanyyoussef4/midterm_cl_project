# Enhanced Calculator CLI

![CI](https://github.com/<your-username>/calculator-cli/actions/workflows/python-app.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

> **Midterm Project – Advanced Command‑Line Calculator**
> Design patterns · Undo/Redo · Observer logging · 100 % test coverage

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features & Design Patterns](#features--design-patterns)
3. [Folder Structure](#folder-structure)
4. [Installation](#installation)
      • [macOS / Linux](#macos--linux) • [Windows (‑PowerShell)](#windows)
5. [Configuration](#configuration)
6. [Using the CLI](#using-the-cli)
7. [Testing & Coverage](#testing--coverage)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [Extending the Calculator](#extending-the-calculator)
10. [License](#license)

---

## Project Overview

This repository contains a **fully‑featured command‑line calculator** that demonstrates professional Python practices and the design‑pattern requirements of the mid‑term assignment:

* **Factory Pattern** – dynamically instantiates 11 arithmetic operations.
* **Memento Pattern** – records every calculation in an undo/redo stack.
* **Observer Pattern** – pluggable observers for logging and auto‑saving.
* **REPL** – colourised, user‑friendly loop with `help`, `undo`, `redo`, `save`, `load`, *etc.*
* **100 % automated test coverage** enforced by GitHub Actions.

> **Learning outcomes met:** Git workflow, CI/CD, design patterns, REPL development, CSV manipulation, unit‑testing, logging, dotenv‑based configuration.

---

## Features & Design Patterns

| Layer        | Key Objects                           | Pattern      | Responsibilities                              |
| ------------ | ------------------------------------- | ------------ | --------------------------------------------- |
| *Operations* | `Operation` ABC; `Add`, `Divide`, …   | **Factory**  | Validates arity, executes arithmetic          |
| *History*    | `History` stack; `CalculationMemento` | **Memento**  | Push / undo / redo calculations               |
| *Observers*  | `LoggingObserver`, `AutoSaveObserver` | **Observer** | React to each new memento                     |
| *CLI*        | `CalculatorCLI`                       | –            | Colour banner, command parsing, `save`/`load` |

---

## Folder Structure

```
calculator-cli/
│  .coveragerc         # coverage rules
│  README.md           # ← you are here
│  requirements.txt    # runtime + dev dependencies
│  .github/workflows/
│     python-app.yml   # CI pipeline
│
├─ app/                # application package
│  ├─ operations.py          # 11 operations + factory
│  ├─ history.py             # undo/redo stack
│  ├─ calculation.py         # Memento dataclass
│  ├─ observers.py           # observers & ABC
│  ├─ calculator.py          # façade (history + observers)
│  ├─ calculator_repl.py     # interactive CLI
│  └─ __init__.py
│
└─ tests/              # 47 pytest cases (100 % cover)
   ├─ test_operations.py
   ├─ test_history.py
   ├─ test_observers.py
   ├─ test_cli_save_load.py
   └─ test_repl_commands.py
```

---

## Installation

### macOS / Linux

```bash
# 1. Clone
$ git clone https://github.com/<your-username>/calculator-cli.git
$ cd calculator-cli

# 2. Create and activate virtual‑env
$ python3 -m venv venv
$ source venv/bin/activate

# 3. Install dependencies (Python 3.9+)
(venv)$ pip install -r requirements.txt

# 4. Copy env template (optional)
(venv)$ cp .env.example .env
# edit values if you need custom paths or history size
```

### Windows (`PowerShell`)

```powershell
# Clone repo
git clone https://github.com/<your-username>/calculator-cli.git
cd calculator-cli

# Create venv (Python >= 3.9)
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Optional: config file
copy .env.example .env
```

> **Note**: Colour output on Windows 10+ is enabled automatically via `colorama`.

---

## Configuration

All configuration is dotenv‑driven. Edit `.env` (or keep defaults).

| Variable                      | Default   | Description                           |
| ----------------------------- | --------- | ------------------------------------- |
| `CALCULATOR_LOG_DIR`          | `logs`    | Where `calculator.log` is written     |
| `CALCULATOR_HISTORY_DIR`      | `history` | CSV auto‑save directory               |
| `CALCULATOR_MAX_HISTORY_SIZE` | `100`     | Max mementos stored (older ones drop) |
| `CALCULATOR_AUTO_SAVE`        | `true`    | Toggle AutoSave observer              |

---

## Using the CLI

```bash
(venv)$ python -m app.calculator_repl
```

```
╔═════════════════════════════════════════════════╗
║           Welcome to the Enhanced CLI!          ║
╚═════════════════════════════════════════════════╝
Type 'help' to list commands – Ctrl‑D or 'exit' to quit.

calc> add 2 3
= 5
calc> power 2 5
= 32
calc> divide 5 0
Error: dividing by zero is not allowed
calc> history
  1: … | ADD 2, 3 = 5
  2: … | POWER 2, 5 = 32
calc> save results.csv
History saved to results.csv
calc> clear
History cleared.
calc> load results.csv
History loaded from results.csv
calc> undo / redo / exit
```

### Command Reference

| Command                                           | Description                 |
| ------------------------------------------------- | --------------------------- |
| `add, subtract, multiply, divide, power, root`, … | perform calculation         |
| `history`                                         | list previous calculations  |
| `undo / redo`                                     | navigate history            |
| `clear`                                           | flush history               |
| `save <file>`                                     | save history → CSV          |
| `load <file>`                                     | load CSV (replaces history) |
| `help`                                            | show help                   |
| `exit / quit`                                     | leave program               |

Logs are written to **`logs/calculator.log`**; CSV snapshots to **`history/history.csv`** (paths configurable).

---

## Testing & Coverage

```bash
(venv)$ pytest --cov app --cov-config=.coveragerc --cov-report term-missing
```

* 47 tests – operations, history, observers, save/load, REPL helpers.
* **100 % line & branch coverage**.
* Coverage gate (`--cov-fail-under=90`) enforced in CI.

---

## CI/CD Pipeline

* **GitHub Actions** – `.github/workflows/python-app.yml`

  * Check‑out → set‑up Python → install deps
  * `pytest` with coverage; build fails < 90 %
  * Status & coverage badge shown on top of this README.

---

## Extending the Calculator

* **Decorator Pattern** – auto‑generate `help` table from registered operations.
* **Colour Themes** – extend `CalculatorCLI` with more `colorama` styles.
* **Packaging** – add `pyproject.toml` and expose CLI via `console_scripts`.

PRs are welcome – remember to keep coverage ≥ 90 %.

---

## License

MIT © 2025 Hany Youssef — feel free to use, learn from, and extend.
