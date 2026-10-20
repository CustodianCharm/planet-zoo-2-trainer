"""Attach to the Planet Zoo 2 process and expose a memory reader/writer."""
from __future__ import annotations

import ctypes
from dataclasses import dataclass
from ctypes import wintypes

import pymem

PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_QUERY_INFORMATION = 0x0400


@dataclass
class AttachResult:
    ok: bool
    pid: int = 0
    reason: str = ""


class ZooAttacher:
    """Thin wrapper over pymem that owns the handle lifecycle."""

    def __init__(self, process_name: str = "PlanetZoo2.exe") -> None:
        self.process_name = process_name
        self._pm: pymem.Pymem | None = None
        self._pid: int = 0

    def attach(self) -> bool:
        try:
            self._pm = pymem.Pymem(self.process_name)
            self._pid = self._pm.process_id
            return True
        except pymem.exception.ProcessNotFound:
            return False
        except pymem.exception.CouldNotOpenProcess:
            return False

    def game_build(self) -> str:
        """Read the build string from the process environment block."""
        if not self._pm:
            return "unknown"
        try:
            env = self._pm.read_string(self._pm.base_address + 0x0, 32)
            return env.split("\x00")[0] or "unknown"
        except Exception:
            return "unknown"

    @property
    def pid(self) -> int:
        return self._pid

    def read(self, address: int, size: int) -> bytes:
        if not self._pm:
            raise RuntimeError("not attached")
        return self._pm.read_bytes(address, size)

    def write(self, address: int, data: bytes) -> None:
        if not self._pm:
            raise RuntimeError("not attached")
        self._pm.write_bytes(address, data, len(data))

    def module_base(self, module: str = "PlanetZoo2.exe") -> int:
        if not self._pm:
            raise RuntimeError("not attached")
        return self._pm.module_base(module)

    def detach(self) -> None:
        if self._pm:
            self._pm.close_process()
            self._pm = None
            self._pid = 0