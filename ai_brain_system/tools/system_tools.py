"""System-level tool functions."""
from __future__ import annotations

import subprocess


class SystemTools:
    """Execute shell commands in a controlled manner."""

    @staticmethod
    def run_command(command: str, timeout: int = 15) -> dict[str, str | int]:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
