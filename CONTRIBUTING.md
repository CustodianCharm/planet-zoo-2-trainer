# Contributing to Planet Zoo 2 Trainer

Thanks for your interest in improving the trainer. This project is a
community-driven, reverse-engineering and modding effort for Planet Zoo 2
(single-player only). Contributions that add new cheats, fix broken
signatures after game patches, or improve the overlay are welcome.

## Ground rules

- **Single-player only.** Do not submit features that affect
  Franchise / online co-op sessions. Pull requests targeting networked
  modes will be closed without review.
- **No game asset redistribution.** Ship offset tables and signatures,
  never ripped `.ovl` / `.blb` files.
- **Keep it readable.** Handler code lives in `src/handlers`, business
  logic in `src/services`. Handlers should be < 40 lines and delegate.

## Workflow

1. Fork and branch from `main` (`feat/cheat-money-boost`).
2. Run `python -m pytest tests/` before opening a PR.
3. If you add a new cheat, drop a signature in `src/offsets/` and a
   matching handler in `src/handlers/`.
4. Attach a short clip or log excerpt showing the feature working.

## Signature updates

When the game patches, `aob_scan.py` will report misses. Update
`src/offsets/signatures.py` and bump `GAME_BUILD` in
`src/offsets/build.py`. Include the new build number in the commit
message (e.g. `offsets: update for build 1.12.3`).

## Code style

- `ruff` for linting, `black` for formatting.
- Type hints on all public functions.
- No bare `except:` — log and re-raise.