#!/usr/bin/env python3
import curses, time


def read_net():
    out = {}
    with open('/proc/net/dev') as f:
        for line in f.readlines()[2:]:
            name, data = line.split(':', 1)
            nums = list(map(int, data.split()))
            out[name.strip()] = (nums[0], nums[8])
    return out


def human(n):
    for unit in ['B/s','KB/s','MB/s','GB/s']:
        if n < 1024:
            return f'{n:6.1f} {unit}'
        n /= 1024
    return f'{n:6.1f} TB/s'


def bar(v, maxv, width=24):
    fill = 0 if maxv <= 0 else int(width * v / maxv)
    return '#' * fill + '-' * (width - fill)


def draw(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    prev = read_net(); t0 = time.time()
    while True:
        time.sleep(1)
        cur = read_net(); t1 = time.time(); dt = max(0.1, t1-t0)
        rows = []
        for iface, vals in cur.items():
            if iface == 'lo' or iface not in prev: continue
            rx = (vals[0]-prev[iface][0]) / dt
            tx = (vals[1]-prev[iface][1]) / dt
            rows.append((iface, rx, tx))
        maxv = max([r[1]+r[2] for r in rows] or [1])
        prev, t0 = cur, t1
        stdscr.erase()
        stdscr.addstr(0, 2, 'ASCII NETWATCH - q to quit')
        stdscr.addstr(2, 2, 'IFACE        RX          TX          TRAFFIC')
        for i, (iface, rx, tx) in enumerate(rows[:curses.LINES-4], 3):
            stdscr.addstr(i, 2, f'{iface:<10} {human(rx)} {human(tx)}  [{bar(rx+tx, maxv)}]')
        if stdscr.getch() in (ord('q'), ord('Q')):
            break


if __name__ == '__main__':
    curses.wrapper(draw)
