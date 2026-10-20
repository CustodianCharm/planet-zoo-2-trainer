"""Optional global hotkey dispatch (F1–F8) that routes to TrainerService."""
from __future__ import annotations

import threading

import keyboard

from src.services.trainer_service import TrainerService

DEFAULT_BINDINGS = {
    "f1": "unlimited_currency",
    "f2": "money_boost",
    "f3": "instant_build",
    "f4": "no_conservation_penalty",
}


class HotkeyHandler:
    def __init__(self, service: TrainerService, bindings: dict[str, str] | None = None) -> None:
        self.service = service
        self.bindings = bindings or DEFAULT_BINDINGS
        self._thread: threading.Thread | None = None

    def _toggle(self, cheat: str) -> None:
        if cheat in self.service.state.active_cheats:
            self.service.revert(cheat)
        else:
            self.service.apply(cheat)

    def start(self) -> None:
        for key, cheat in self.bindings.items():
            keyboard.add_hotkey(key, self._toggle, args=(cheat,), suppress=False)

    def stop(self) -> None:
        keyboard.unhook_all_hotkeys()