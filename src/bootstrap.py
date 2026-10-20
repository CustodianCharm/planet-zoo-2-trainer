"""Entry bootstrap: elevation check, process attach, service graph wiring."""
from __future__ import annotations

import ctypes
import sys
from pathlib import Path

from rich.console import Console

from src.offsets.build import GAME_BUILD, SUPPORTED_BUILDS
from src.process.attacher import ZooAttacher
from src.services.trainer_service import TrainerService
from src.handlers.console_handler import ConsoleHandler

console = Console()


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not is_admin():
        console.print("[red]Trainer requires Administrator.[/red] Restart as admin.")
        return 2

    attacher = ZooAttacher(process_name="PlanetZoo2.exe")
    if not attacher.attach():
        console.print("[red]PlanetZoo2.exe not found.[/red] Launch the game first.")
        return 3

    detected = attacher.game_build()
    if detected not in SUPPORTED_BUILDS:
        console.print(
            f"[yellow]Untested build {detected}[/yellow] "
            f"(offsets pinned to {GAME_BUILD}). Cheats may be unstable."
        )

    service = TrainerService(attacher, log_dir=Path("logs"))
    handler = ConsoleHandler(service)
    return handler.run(argv)


if __name__ == "__main__":
    raise SystemExit(main())