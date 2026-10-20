"""Read/write wrapper that resolves signatures into concrete addresses."""
from __future__ import annotations

import struct

from src.process.attacher import ZooAttacher
from src.offsets.signatures import Signature


class MemoryPatcher:
    def __init__(self, attacher: ZooAttacher) -> None:
        self.attacher = attacher
        self._original: dict[str, bytes] = {}

    def _resolve(self, sig: Signature) -> int:
        base = self.attacher.module_base(sig.module)
        pattern = bytes.fromhex(sig.aob)
        mask = sig.mask
        window = self.attacher.read(base, 0x1000000)
        for i in range(len(window) - len(pattern)):
            for j, (b, m) in enumerate(zip(pattern, mask)):
                if m == "?":
                    continue
                if window[i + j] != b:
                    break
            else:
                return base + i + sig.offset
        raise LookupError(f"signature {sig.name} not found")

    def apply(self, sig: Signature, value: float | None = None) -> bool:
        try:
            addr = self._resolve(sig)
            self._original.setdefault(sig.name, self.attacher.read(addr, sig.size))
            if sig.value_type == "f32" and value is not None:
                payload = struct.pack("<f", value)
            elif sig.value_type == "i32" and value is not None:
                payload = struct.pack("<i", int(value))
            else:
                payload = bytes.fromhex(sig.patch)
            self.attacher.write(addr, payload)
            return True
        except (LookupError, OSError) as exc:
            return False

    def revert(self, sig: Signature) -> bool:
        orig = self._original.pop(sig.name, None)
        if orig is None:
            return False
        try:
            addr = self._resolve(sig)
            self.attacher.write(addr, orig)
            return True
        except (LookupError, OSError):
            return False