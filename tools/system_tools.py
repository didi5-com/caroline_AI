"""System automation tools."""
from __future__ import annotations

import subprocess


def open_app(app_name: str) -> str:
    return f"Open app requested: {app_name}"


def run_command(command: str) -> str:
    proc = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return proc.stderr.strip() or f"Command failed ({proc.returncode})"
    return proc.stdout.strip() or "Command executed"
