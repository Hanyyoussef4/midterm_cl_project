#!/usr/bin/env python3
import runpy

if __name__ == "__main__":
    # exactly the same as: python -m app.calculator_repl
    runpy.run_module("app.calculator_repl", run_name="__main__")
