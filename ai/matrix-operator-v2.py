#!/usr/bin/env python3
"""
Operator Console Matrix Screensaver v2

Controls:
    q / Q / Esc   Quit

Features:
- Half-width Katakana matrix rain
- Independent column speeds and trail lengths
- Personalized startup sequence using account name
- Left-side system log panel
- Right-side diagnostics / meter panel
- HUD frame, clock, rotating status bar
- Horizontal glitch sweeps, scan shimmer, sparkles
- Subliminal quit hint hidden in the rain
- Defensive curses handling for macOS terminals
"""

import curses
import getpass
import os
import pwd
import random
import time


GLYPHS = (
    "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ"
    "ﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓ"
    "ﾔﾕﾖﾗﾘﾙﾚﾛﾜ"
    "0123456789"
    "@#$%&*+=-:;<>?/|[]{}"
)
GLITCH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

STATUSES = [
    "TRACE ROUTE ACTIVE",
    "SIGNAL LOCK ACQUIRED",
    "DECRYPTING RELAY",
    "MIRROR NODE ONLINE",
    "PACKET VEIL STABLE",
    "CARRIER WAVE NOMINAL",
    "GHOST HANDSHAKE OK",
    "MAINFRAME ECHO DETECTED",
    "PROXY STACK ROTATING",
    "SENTINEL SWEEP AVOIDED",
]

LOG_MESSAGES = [
    "routing carrier burst",
    "masking outbound signature",
    "synchronizing relay keys",
    "observing upstream mirror",
    "injecting null packets",
    "rebuilding cipher lattice",
    "parsing machine code rain",
    "monitoring backbone chatter",
    "auth token accepted",
    "auth token rejected",
    "falling back to shadow path",
    "tracking residual trace",
    "reframing packet envelope",
    "spoofing operator heartbeat",
    "rewriting session fingerprint",
]

BANNERS = [
    "ACCESSING MAINFRAME",
    "CONSTRUCT LOAD READY",
    "REDPILL HANDSHAKE",
    "TRACE MASK ENGAGED",
    "OPERATOR LINK STABLE",
]


def get_first_name():
    """Try full account name first, then fall back to login name."""
    try:
        gecos = pwd.getpwuid(os.getuid()).pw_gecos
        full_name = gecos.split(",")[0].strip()
        if full_name:
            return full_name.split()[0].capitalize()
    except Exception:
        pass
    try:
        user = getpass.getuser().strip()
        if user:
            return user.split()[0].capitalize()
    except Exception:
        pass
    return "Operator"


def safe_curs_set(value: int) -> None:
    try:
        curses.curs_set(value)
    except curses.error:
        pass


def init_colors():
    green_dim = green = green_bold = white_bold = curses.A_NORMAL
    if curses.has_colors():
        try:
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_WHITE, -1)
            green = curses.color_pair(1)
            green_bold = green | curses.A_BOLD
            green_dim = green | curses.A_DIM
            white_bold = curses.color_pair(2) | curses.A_BOLD
        except curses.error:
            pass
    return green_dim, green, green_bold, white_bold


def draw_text(stdscr, y: int, x: int, text: str, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    if x < 0:
        text = text[-x:]
        x = 0
    if not text:
        return
    try:
        stdscr.addnstr(y, x, text, max(0, w - x), attr)
    except curses.error:
        pass


def draw_box(stdscr, top: int, left: int, height: int, width: int, attr=0):
    if height < 2 or width < 2:
        return
    for x in range(left + 1, left + width - 1):
        draw_text(stdscr, top, x, "-", attr)
        draw_text(stdscr, top + height - 1, x, "-", attr)
    for y in range(top + 1, top + height - 1):
        draw_text(stdscr, y, left, "|", attr)
        draw_text(stdscr, y, left + width - 1, "|", attr)
    draw_text(stdscr, top, left, "+", attr)
    draw_text(stdscr, top, left + width - 1, "+", attr)
    draw_text(stdscr, top + height - 1, left, "+", attr)
    draw_text(stdscr, top + height - 1, left + width - 1, "+", attr)


def clamp(n, lo, hi):
    return max(lo, min(hi, n))


class Column:
    def __init__(self, top: int, bottom: int):
        self.top = top
        self.bottom = bottom
        self.reset(fresh=True)

    @property
    def height(self):
        return self.bottom - self.top

    def reset(self, fresh: bool = False) -> None:
        h = max(1, self.height)
        self.head_y = random.randint(self.top - h, self.top) if fresh else self.top - random.randint(4, h // 2 + 8)
        self.speed = random.randint(1, 5)
        self.length = random.randint(7, 24)
        self.tick = 0
        self.glyphs = [self.next_glyph() for _ in range(self.length)]

    def next_glyph(self) -> str:
        return random.choice(GLYPHS if random.random() < 0.95 else GLITCH)

    def ready(self) -> bool:
        self.tick += 1
        if self.tick < self.speed:
            return False
        self.tick = 0
        return True

    def advance(self) -> None:
        self.head_y += 1
        self.glyphs.insert(0, self.next_glyph())
        if len(self.glyphs) > self.length:
            self.glyphs.pop()

    def offscreen(self) -> bool:
        return self.head_y - self.length > self.bottom


class LogPanel:
    def __init__(self, rows: int):
        self.rows = rows
        self.lines = []
        self.last_update = 0.0

    def add(self, text: str) -> None:
        stamp = time.strftime("%H:%M:%S")
        self.lines.append(f"[{stamp}] {text}")
        self.lines = self.lines[-self.rows:]

    def maybe_update(self) -> None:
        now = time.monotonic()
        if now - self.last_update > random.uniform(0.35, 1.1):
            self.last_update = now
            msg = random.choice(LOG_MESSAGES)
            if random.random() < 0.25:
                msg += f" :: {random.randint(1000, 9999):04X}"
            self.add(msg)


class Meter:
    def __init__(self, value=None):
        self.value = random.randint(20, 80) if value is None else value

    def update(self, jitter=6):
        self.value = clamp(self.value + random.randint(-jitter, jitter), 0, 100)


class TraceGraph:
    def __init__(self, width: int):
        self.width = max(8, width)
        self.values = [random.randint(20, 80) for _ in range(self.width)]

    def update(self):
        nxt = clamp(self.values[-1] + random.randint(-12, 12), 0, 100)
        self.values.append(nxt)
        self.values = self.values[-self.width:]


def meter_bar(value: int, width: int) -> str:
    filled = int(width * value / 100)
    return "[" + ("#" * filled).ljust(width) + f"] {value:3d}%"


def sparkline(values) -> str:
    chars = " .:-=+*#%@"
    out = []
    for v in values:
        idx = int(v / 100 * (len(chars) - 1))
        out.append(chars[idx])
    return "".join(out)


def draw_column(stdscr, x: int, col: Column, attrs) -> None:
    green_dim, green, green_bold, white_bold = attrs
    for i in range(col.length):
        y = col.head_y - i
        if y < col.top:
            continue
        if y >= col.bottom:
            break

        if i > 0 and random.random() < 0.035:
            col.glyphs[i] = col.next_glyph()

        ch = col.glyphs[i]
        if i == 0:
            attr = white_bold
        elif i <= 2:
            attr = green_bold
        elif i < col.length * 0.55:
            attr = green
        else:
            attr = green_dim

        try:
            stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass

    tail_y = col.head_y - col.length
    if col.top <= tail_y < col.bottom:
        try:
            stdscr.addch(tail_y, x, " ")
        except curses.error:
            pass


def boot_sequence(stdscr, attrs) -> None:
    green_dim, green, green_bold, _ = attrs
    h, w = stdscr.getmaxyx()
    name = get_first_name()

    title = random.choice([
        f"WAKE UP, {name.upper()}...",
        f"{name.upper()}, THE MATRIX HAS YOU...",
        f"HELLO, {name.upper()}...",
        f"GOOD EVENING, {name.upper()}...",
    ])
    subtitle = random.choice([
        "FOLLOW THE WHITE RABBIT",
        "SIGNAL ACQUIRED",
        "OPERATOR LINK ESTABLISHED",
        "STANDBY FOR CONSTRUCT LOAD",
    ])
    hint = "q quits"

    lines = [
        (title, green_bold),
        ("", green),
        (subtitle, green),
        ("", green),
        (hint, green_dim),
    ]

    stdscr.erase()
    start_y = max(1, h // 2 - len(lines) // 2)

    for row, (text, attr) in enumerate(lines):
        x0 = max(0, (w - len(text)) // 2)
        for i, ch in enumerate(text):
            try:
                stdscr.addch(start_y + row, x0 + i, ch, attr)
            except curses.error:
                pass
            stdscr.refresh()
            curses.napms(14)
        curses.napms(70)

    end = time.monotonic() + 1.0
    while time.monotonic() < end:
        if stdscr.getch() in (27, ord("q"), ord("Q")):
            raise KeyboardInterrupt
        curses.napms(20)

    for _ in range(7):
        for row, (text, attr) in enumerate(lines):
            x0 = max(0, (w - len(text)) // 2)
            for i, ch in enumerate(text):
                shown = random.choice(GLITCH) if random.random() < 0.4 else ch
                try:
                    stdscr.addch(start_y + row, x0 + i, shown, attr)
                except curses.error:
                    pass
        stdscr.refresh()
        curses.napms(45)

    stdscr.erase()
    stdscr.refresh()


def maybe_draw_quit_hint(stdscr, left: int, right: int, top: int, bottom: int, attr) -> None:
    if right - left > 8 and bottom - top > 8 and random.random() < 0.012:
        x = random.randint(left + 1, right - 2)
        y = random.randint(top + 1, bottom - 2)
        try:
            stdscr.addch(y, x, "Q", attr)
        except curses.error:
            pass


def maybe_glitch_sweep(stdscr, left: int, right: int, top: int, bottom: int, attrs) -> None:
    _, green, green_bold, white_bold = attrs
    if random.random() >= 0.018 or right - left < 12 or bottom - top < 5:
        return
    y = random.randint(top + 1, bottom - 2)
    start = random.randint(left, max(left, right - 10))
    length = random.randint(8, min(34, right - start))
    for x in range(start, start + length):
        ch = random.choice(GLITCH + GLYPHS)
        attr = random.choice((green, green_bold, white_bold))
        try:
            stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass


def maybe_status_banner(stdscr, left: int, right: int, y: int, attrs) -> None:
    green_dim, _, green_bold, _ = attrs
    if random.random() >= 0.01 or right - left < 24:
        return
    text = f"[ {random.choice(BANNERS)} ]"
    x = left + max(1, (right - left - len(text)) // 2)
    draw_text(stdscr, y, x, text, green_bold if random.random() < 0.5 else green_dim)


def draw_hud(stdscr, attrs, status_text: str) -> None:
    green_dim, green, green_bold, _ = attrs
    h, w = stdscr.getmaxyx()

    draw_box(stdscr, 0, 0, h, w, green_dim)

    clock_text = time.strftime("%Y-%m-%d %H:%M:%S")
    draw_text(stdscr, 0, 2, " OPERATOR CONSOLE V2 ", green_bold)
    draw_text(stdscr, 0, max(2, w - len(clock_text) - 2), clock_text, green)

    bottom = f" STATUS: {status_text} "
    quit_hint = " Q TO EXIT "
    draw_text(stdscr, h - 1, 2, bottom, green)
    draw_text(stdscr, h - 1, max(2, w - len(quit_hint) - 2), quit_hint, green_dim)


def draw_log_panel(stdscr, panel, top: int, left: int, height: int, width: int, attrs) -> None:
    green_dim, green, _, _ = attrs
    if height < 4 or width < 16:
        return
    draw_box(stdscr, top, left, height, width, green_dim)
    draw_text(stdscr, top, left + 2, " SYSTEM LOG ", green)
    visible = panel.lines[-(height - 2):]
    for i, line in enumerate(visible, start=1):
        draw_text(stdscr, top + i, left + 1, line, green_dim if i < len(visible) else green)


def draw_diag_panel(stdscr, top: int, left: int, height: int, width: int, attrs, meters, graphs, status_text: str) -> None:
    green_dim, green, green_bold, _ = attrs
    if height < 10 or width < 20:
        return

    draw_box(stdscr, top, left, height, width, green_dim)
    draw_text(stdscr, top, left + 2, " DIAGNOSTICS ", green)

    row = top + 1
    draw_text(stdscr, row, left + 1, f"NODE   : {status_text[:width - 10]}", green_bold); row += 1
    draw_text(stdscr, row, left + 1, f"CPU    : {meter_bar(meters['cpu'].value, max(6, width - 13))}", green); row += 1
    draw_text(stdscr, row, left + 1, f"NET    : {meter_bar(meters['net'].value, max(6, width - 13))}", green); row += 1
    draw_text(stdscr, row, left + 1, f"TRACE  : {meter_bar(meters['trace'].value, max(6, width - 13))}", green); row += 1
    draw_text(stdscr, row, left + 1, f"ENTROPY: {meter_bar(meters['entropy'].value, max(6, width - 13))}", green); row += 2

    draw_text(stdscr, row, left + 1, " CPU HISTORY ", green_bold); row += 1
    draw_text(stdscr, row, left + 1, sparkline(graphs['cpu'].values[:width - 2]), green_dim); row += 1

    draw_text(stdscr, row, left + 1, " NET HISTORY ", green_bold); row += 1
    draw_text(stdscr, row, left + 1, sparkline(graphs['net'].values[:width - 2]), green_dim); row += 1

    draw_text(stdscr, row, left + 1, " TRACE GRAPH ", green_bold); row += 1
    draw_text(stdscr, row, left + 1, sparkline(graphs['trace'].values[:width - 2]), green_dim); row += 1

    if row < top + height - 1:
        draw_text(stdscr, row, left + 1, f"TOKEN  : {random.randint(1000, 65535):04X}", green_dim)


def draw_scanlines(stdscr, left: int, right: int, top: int, bottom: int, attrs) -> None:
    green_dim, _, _, _ = attrs
    if random.random() < 0.65:
        for y in range(top + 1, bottom - 1, 4):
            if random.random() < 0.25:
                x = random.randint(left + 1, max(left + 1, right - 8))
                draw_text(stdscr, y, x, random.choice(["....", "::", "..::..", "-----"]), green_dim)


def build_columns(left: int, right: int, top: int, bottom: int):
    return [Column(top, bottom) for _ in range(max(0, right - left))]


def main(stdscr) -> None:
    safe_curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    attrs = init_colors()
    green_dim, green, green_bold, white_bold = attrs

    try:
        boot_sequence(stdscr, attrs)
    except KeyboardInterrupt:
        return

    h, w = stdscr.getmaxyx()

    panel_w = min(42, max(20, w // 4))
    left_w = panel_w if w >= 80 else 0
    right_w = panel_w if w >= 110 else 0

    rain_left = 1 + left_w
    rain_right = w - 1 - right_w
    rain_top = 1
    rain_bottom = h - 1

    columns = build_columns(rain_left, rain_right, rain_top, rain_bottom)

    log_panel = LogPanel(rows=max(4, h - 6))
    for _ in range(6):
        log_panel.maybe_update()

    meters = {
        "cpu": Meter(),
        "net": Meter(),
        "trace": Meter(),
        "entropy": Meter(),
    }
    graphs = {
        "cpu": TraceGraph(max(8, right_w - 2)),
        "net": TraceGraph(max(8, right_w - 2)),
        "trace": TraceGraph(max(8, right_w - 2)),
    }

    status_text = random.choice(STATUSES)
    last_resize_check = time.monotonic()
    last_status_change = 0.0
    last_metric_update = 0.0

    while True:
        now = time.monotonic()

        if now - last_resize_check > 0.2:
            new_h, new_w = stdscr.getmaxyx()
            if (new_h, new_w) != (h, w):
                h, w = new_h, new_w
                stdscr.erase()

                panel_w = min(42, max(20, w // 4))
                left_w = panel_w if w >= 80 else 0
                right_w = panel_w if w >= 110 else 0

                rain_left = 1 + left_w
                rain_right = w - 1 - right_w
                rain_top = 1
                rain_bottom = h - 1

                columns = build_columns(rain_left, rain_right, rain_top, rain_bottom)
                log_panel.rows = max(4, h - 6)
                graphs = {
                    "cpu": TraceGraph(max(8, right_w - 2)),
                    "net": TraceGraph(max(8, right_w - 2)),
                    "trace": TraceGraph(max(8, right_w - 2)),
                }
            last_resize_check = now

        if now - last_status_change > random.uniform(3.5, 7.5):
            status_text = random.choice(STATUSES)
            last_status_change = now

        if now - last_metric_update > 0.25:
            for meter in meters.values():
                meter.update()
            for graph in graphs.values():
                graph.update()
            last_metric_update = now

        log_panel.maybe_update()

        for i, col in enumerate(columns):
            if not col.ready():
                continue
            col.advance()
            draw_column(stdscr, rain_left + i, col, attrs)
            if col.offscreen():
                col.reset()

        draw_scanlines(stdscr, rain_left, rain_right, rain_top, rain_bottom, attrs)
        maybe_glitch_sweep(stdscr, rain_left, rain_right, rain_top, rain_bottom, attrs)
        maybe_draw_quit_hint(stdscr, rain_left, rain_right, rain_top, rain_bottom, green_dim)
        maybe_status_banner(stdscr, rain_left, rain_right, 1, attrs)

        if random.random() < 0.04 and rain_right - rain_left > 4 and rain_bottom - rain_top > 4:
            x = random.randint(rain_left + 1, rain_right - 2)
            y = random.randint(rain_top + 1, rain_bottom - 2)
            try:
                stdscr.addch(y, x, random.choice(GLYPHS), white_bold if random.random() < 0.3 else green_bold)
            except curses.error:
                pass

        if left_w:
            draw_log_panel(stdscr, log_panel, 2, 1, h - 4, left_w, attrs)
        if right_w:
            draw_diag_panel(stdscr, 2, w - right_w - 1, h - 4, right_w, attrs, meters, graphs, status_text)

        draw_hud(stdscr, attrs, status_text)

        try:
            stdscr.refresh()
        except curses.error:
            pass

        key = stdscr.getch()
        if key in (27, ord("q"), ord("Q")):
            break

        curses.napms(42)


if __name__ == "__main__":
    curses.wrapper(main)
