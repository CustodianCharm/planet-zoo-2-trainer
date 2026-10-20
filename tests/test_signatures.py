from src.offsets.signatures import SIGNATURES
from src.offsets.aob_scan import compile_pattern
from src.offsets.build import GAME_BUILD, SUPPORTED_BUILDS


def test_signature_table_nonempty():
    assert len(SIGNATURES) >= 3


def test_masks_match_aob_lengths():
    for sig in SIGNATURES:
        assert len(sig.aob.split()) == len(sig.mask), sig.name


def test_all_signatures_compile():
    for sig in SIGNATURES:
        pat = compile_pattern(sig.aob, sig.mask)
        assert pat.pattern


def test_supported_builds_contains_current():
    assert GAME_BUILD in SUPPORTED_BUILDS


def test_signature_builds_are_known():
    for sig in SIGNATURES:
        for b in sig.builds:
            assert b == "any" or b in SUPPORTED_BUILDS, (sig.name, b)