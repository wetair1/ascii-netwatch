# ascii-netwatch

ASCII curses network activity watcher for Linux terminals.

## Features

- Live RX/TX speed per interface
- ASCII traffic bars
- Ignores loopback by default
- Pure Python stdlib
- No psutil, no dependencies

## Usage

```bash
python3 main.py
```

Press `q` to quit.

## Notes

Network counters are read from `/proc/net/dev`.
