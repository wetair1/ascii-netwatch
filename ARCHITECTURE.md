# Architecture

ascii-netwatch is a small curses application that watches Linux network counters without external dependencies.

## Runtime flow

1. `curses.wrapper(draw)` starts the terminal UI.
2. The app reads interface counters from `/proc/net/dev`.
3. Two snapshots are compared to calculate RX/TX speed.
4. The screen is redrawn once per tick with ASCII traffic bars.
5. Pressing `q` exits the loop.

## Main parts

- `read_net()` parses `/proc/net/dev` and returns byte counters per interface.
- `human()` formats bytes per second into readable units.
- `bar()` renders traffic intensity as an ASCII bar.
- `draw()` owns the curses loop, refresh timing and keyboard handling.

## Design rules

- Keep dependencies at zero.
- Keep polling simple and predictable.
- Ignore loopback by default to reduce noise.
- Keep Linux-specific parsing isolated in one function.
- Keep the UI readable on narrow terminals.
