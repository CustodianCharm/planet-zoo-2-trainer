"""Standalone AOB scanner used by tests and the maintenance CLI."""
from __future__ import annotations

import re
import sys

from src.offsets.signatures import SIGNATURES


def parse_mask(mask: str) -> bytes:
    return mask.encode()


def compile_pattern(aob: str, mask: str) -> re.Pattern[bytes]:
    tokens = aob.split()
    out = bytearray()
    for tok, m in zip(tokens, mask):
        if m == "?":
            out.append(0x2E)
        else:
            out.append(int(tok, 16))
    return re.compile(bytes(out), re.DOTALL)


def scan(buffer: bytes, sig) -> int:
    pat = compile_pattern(sig.aob, sig.mask)
    m = pat.search(buffer)
    return m.start() if m else -1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: aob_scan.py <dump.bin> [signature]")
        return 1
    with open(argv[1], "rb") as f:
        buf = f.read()
    for sig in SIGNATURES:
        if len(argv) > 2 and sig.name != argv[2]:
            continue
        off = scan(buf, sig)
        print(f"{sig.name:32s} {'miss' if off < 0 else f'0x{off:x}'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))