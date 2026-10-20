from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

PatchKind = Literal["nop", "float", "int", "bytes"]


@dataclass
class PatchStep:
    signature: str
    kind: PatchKind
    payload: bytes
    note: str = ""


@dataclass
class PatchPlan:
    name: str
    steps: list[PatchStep] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add(self, step: PatchStep) -> "PatchPlan":
        self.steps.append(step)
        return self

    def describe(self) -> str:
        lines = [f"plan={self.name} steps={len(self.steps)}"]
        for s in self.steps:
            lines.append(f"  - {s.signature} [{s.kind}] {s.payload.hex()} ({s.note})")
        return "\n".join(lines)