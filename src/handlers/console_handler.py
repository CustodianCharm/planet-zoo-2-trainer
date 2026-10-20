"""Thin CLI handler. All logic lives in TrainerService."""
from __future__ import annotations

import shlex
from typing import Callable

from rich.console import Console
from rich.table import Table

from src.services.trainer_service import TrainerService

console = Console()


class ConsoleHandler:
    def __init__(self, service: TrainerService) -> None:
        self.service = service
        self.commands: dict[str, Callable[[list[str]], int]] = {
            "list": self._cmd_list,
            "apply": self._cmd_apply,
            "revert": self._cmd_revert,
            "revert-all": self._cmd_revert_all,
            "status": self._cmd_status,
            "quit": self._cmd_quit,
        }

    def run(self, _argv: list[str]) -> int:
        console.print("[bold green]Planet Zoo 2 Trainer[/bold green] — type 'help' for commands")
        while True:
            try:
                line = console.input("[cyan]pz2>[/cyan] ").strip()
            except (EOFError, KeyboardInterrupt):
                return 0
            if not line:
                continue
            parts = shlex.split(line)
            cmd, args = parts[0].lower(), parts[1:]
            if cmd == "help":
                self._cmd_help()
                continue
            handler = self.commands.get(cmd)
            if handler is None:
                console.print(f"[red]unknown command: {cmd}[/red]")
                continue
            code = handler(args)
            if code == -1:
                return 0

    def _cmd_list(self, _args: list[str]) -> int:
        table = Table(title="Available cheats")
        table.add_column("Name")
        table.add_column("Status")
        for name in self.service.registry.list_cheats():
            status = "ON" if name in self.service.state.active_cheats else "off"
            table.add_row(name, status)
        console.print(table)
        return 0

    def _cmd_apply(self, args: list[str]) -> int:
        if not args:
            console.print("[red]usage: apply <cheat> [value][/red]")
            return 1
        value = float(args[1]) if len(args) > 1 else None
        ok = self.service.apply(args[0], value)
        console.print("[green]applied[/green]" if ok else "[red]failed[/red]")
        return 0 if ok else 1

    def _cmd_revert(self, args: list[str]) -> int:
        if not args:
            return 1
        return 0 if self.service.revert(args[0]) else 1

    def _cmd_revert_all(self, _args: list[str]) -> int:
        n = self.service.revert_all()
        console.print(f"reverted {n} cheat(s)")
        return 0

    def _cmd_status(self, _args: list[str]) -> int:
        console.print(self.service.state)
        return 0

    def _cmd_quit(self, _args: list[str]) -> int:
        self.service.revert_all()
        return -1

    def _cmd_help(self) -> None:
        console.print("commands: list | apply <cheat> [value] | revert <cheat> | revert-all | status | quit")