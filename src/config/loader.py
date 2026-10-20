from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class TrainerConfig(BaseModel):
    process_name: str = "PlanetZoo2.exe"
    hotkeys_enabled: bool = True
    overlay_enabled: bool = False
    log_level: str = "INFO"
    auto_revert_on_exit: bool = True
    hotkeys: dict[str, str] = Field(default_factory=dict)


def load_config(path: Path | str = Path("config/trainer.yaml")) -> TrainerConfig:
    p = Path(path)
    if not p.exists():
        return TrainerConfig()
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return TrainerConfig(**data)