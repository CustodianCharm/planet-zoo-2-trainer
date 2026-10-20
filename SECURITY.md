# Security Policy

## Scope

Planet Zoo 2 Trainer interacts with the Planet Zoo 2 process via
`OpenProcess` + `ReadProcessMemory` / `WriteProcessMemory`. This is
inherently privileged. The project is scoped to **offline single-player
sandbox and challenge mode only**.

## Reporting a vulnerability

If you find a bug that can crash the game, corrupt a save, or — more
seriously — trigger anti-cheat or telemetry reporting to Frontier, please
**do not open a public issue**. Email `security@planet-zoo-2-trainer.dev`
with:

- Trainer version (`Trainer > About`)
- Game build (`Main menu > bottom-right`)
- Reproduction steps and any logs from `logs/`

We aim to respond within 72 hours.

## Out of scope

- Detection by Frontier services — this trainer does not attempt to
  bypass anti-cheat and will not accept patches that do.
- Online / Franchise mode behavior.
- Redistribution of the trainer binary.

## Disclosure

Coordinated disclosure window is 90 days, or sooner if a fix ships.