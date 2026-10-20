"""Business service layer: owns cheat state, delegates to memory adapters."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from src.process.attacher import ZooAttacher
from src.offsets.build import GAME_BUILD
from src.offsets.signatures import SIGNATURES
from src.services.memory_patch import MemoryPatcher
from src.services.cheat_registry import CheatRegistry


@dataclass
class TrainerState:
    active_cheats: set[str] = field(default_factory=set)
    money_boost: bool = False
    instant_build: bool = False
    unlimited_currency: bool = False
    no_conservation_penalty: bool = False
    time_scale: float = 1.0
    last_patch: str = ""


class TrainerService:
    def __init__(self, attacher: ZooAttacher, log_dir: Path = Path("logs")) -> None:
        self.attacher = attacher
        self.state = TrainerState()
        self.patcher = MemoryPatcher(attacher)
        self.registry = CheatRegistry(SIGNATURES)
        log_dir.mkdir(exist_ok=True)
        self.log_path = log_dir / f"trainer-{datetime.now(timezone.utc):%Y%m%d-%H%M}.log"
        logging.basicConfig(
            filename=self.log_path,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
        )
        self.log = logging.getLogger("trainer")

    def apply(self, cheat: str, value: float | None = None) -> bool:
        sig = self.registry.get(cheat)
        if sig is None:
            self.log.warning("unknown cheat %s", cheat)
            return False
        if not self.registry.is_supported(sig, GAME_BUILD):
            self.log.warning("cheat %s unsupported on build %s", cheat, GAME_BUILD)
            return False
        ok = self.patcher.apply(sig, value)
        if ok:
            self.state.active_cheats.add(cheat)
            self.state.last_patch = datetime.now(timezone.utc).isoformat()
        self.log.info("apply %s value=%s ok=%s", cheat, value, ok)
        return ok

    def revert(self, cheat: str) -> bool:
        sig = self.registry.get(cheat)
        if sig is None:
            return False
        ok = self.patcher.revert(sig)
        if ok:
            self.state.active_cheats.discard(cheat)
        return ok

    def revert_all(self) -> int:
        count = 0
        for cheat in list(self.state.active_cheats):
            if self.revert(cheat):
                count += 1
        return count