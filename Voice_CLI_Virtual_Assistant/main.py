#!/usr/bin/env python3
"""Launcher for the Voice & CLI driven system virtual assistant.

    python main.py                  interactive text session
    python main.py --voice          interactive voice session
    python main.py --say "battery"  single command, then exit
"""

from __future__ import annotations

import sys

from assistant.cli import main

if __name__ == "__main__":
    sys.exit(main())
