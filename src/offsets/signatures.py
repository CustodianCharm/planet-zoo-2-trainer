from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Signature:
    name: str
    module: str
    aob: str
    mask: str
    offset: int
    size: int
    value_type: str = "bytes"
    patch: str = ""
    builds: tuple[str, ...] = ("any",)
    description: str = ""
    tags: list[str] = field(default_factory=list)


SIGNATURES: list[Signature] = [
    Signature(
        name="unlimited_currency",
        module="PlanetZoo2.exe",
        aob="48 8B 05 ? ? ? ? 48 85 C0 74 0F 48 8B 40 08",
        mask="xxx????xxxxxxx",
        offset=0x14,
        size=4,
        value_type="i32",
        builds=("1.12.0", "1.12.1", "1.12.2", "1.12.3"),
        description="Patch the currency cap check to allow INT_MAX.",
        tags=["economy", "single-player"],
    ),
    Signature(
        name="money_boost",
        module="PlanetZoo2.exe",
        aob="F3 0F 10 0D ? ? ? ? F3 0F 59 C1 F3 0F 11 47 20",
        mask="xxxx????xxxxxxxx",
        offset=0x10,
        size=4,
        value_type="f32",
        patch="00 00 80 3F",
        builds=("1.12.2", "1.12.3"),
        description="Overwrite the multiplier to 1.0f to neutralize income scaling.",
        tags=["economy", "single-player"],
    ),
    Signature(
        name="instant_build",
        module="PlanetZoo2.exe",
        aob="E8 ? ? ? ? 84 C0 0F 84 ? ? ? ? 48 8B 4F 10",
        mask="x????xxx????xxxx",
        offset=0x06,
        size=6,
        value_type="bytes",
        patch="90 90 90 90 90 90",
        builds=("1.12.3",),
        description="NOP the build-time gate.",
        tags=["construction", "single-player"],
    ),
    Signature(
        name="no_conservation_penalty",
        module="PlanetZoo2.exe",
        aob="F3 0F 10 15 ? ? ? ? F3 0F 5C D1 F3 0F 11 57 08",
        mask="xxxx????xxxxxxxx",
        offset=0x0C,
        size=4,
        value_type="f32",
        patch="00 00 00 00",
        builds=("1.12.0", "1.12.1", "1.12.2", "1.12.3"),
        description="Zero the conservation penalty accumulator.",
        tags=["conservation", "single-player"],
    ),
    Signature(
        name="time_scale",
        module="PlanetZoo2.exe",
        aob="F3 0F 10 0D ? ? ? ? F3 0F 59 05 ? ? ? ? F3 0F 11 4E 18",
        mask="xxxx????xxxx????xxxx",
        offset=0x08,
        size=4,
        value_type="f32",
        patch="00 00 80 3F",
        builds=("1.12.3",),
        description="Set the global time multiplier.",
        tags=["time", "single-player"],
    ),
]