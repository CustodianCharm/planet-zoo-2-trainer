from pathlib import Path

from src.offsets.signatures import SIGNATURES
from src.services.cheat_registry import CheatRegistry
from src.services.trainer_service import TrainerService


class FakeAttacher:
    process_name = "PlanetZoo2.exe"
    pid = 4242

    def __init__(self) -> None:
        self.writes: list[tuple[int, bytes]] = []
        self._buf = bytes(0x100)

    def read(self, address: int, size: int) -> bytes:
        return self._buf[address : address + size] or bytes(size)

    def write(self, address: int, data: bytes) -> None:
        self.writes.append((address, data))

    def module_base(self, module: str = "PlanetZoo2.exe") -> int:
        return 0

    def game_build(self) -> str:
        return "1.12.3"


def test_registry_lists_cheats():
    reg = CheatRegistry(SIGNATURES)
    assert "unlimited_currency" in reg.list_cheats()
    assert reg.get("does_not_exist") is None


def test_unknown_cheat_is_rejected(tmp_path: Path):
    svc = TrainerService(FakeAttacher(), log_dir=tmp_path)
    assert svc.apply("not_a_cheat") is False


def test_revert_all_is_safe_when_empty(tmp_path: Path):
    svc = TrainerService(FakeAttacher(), log_dir=tmp_path)
    assert svc.revert_all() == 0
    assert svc.state.active_cheats == set()
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>