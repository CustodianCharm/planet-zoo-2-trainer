from __future__ import annotations

from src.offsets.signatures import Signature


class CheatRegistry:
    """Lookup helper around the signature table."""

    def __init__(self, signatures: list[Signature]) -> None:
        self._by_name = {s.name: s for s in signatures}

    def get(self, name: str) -> Signature | None:
        return self._by_name.get(name)

    def is_supported(self, sig: Signature, build: str) -> bool:
        return build in sig.builds or "any" in sig.builds

    def list_cheats(self) -> list[str]:
        return sorted(self._by_name.keys())