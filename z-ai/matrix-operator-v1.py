#!/usr/bin/env python3
"""
Operator Console Matrix Screensaver

Controls:
    q / Q / Esc   Quit

Features:
- Half-width Katakana matrix rain
- Independent column speeds and trail lengths
- Personalized startup sequence using account name
- Randomized intro phrases
- HUD frame, clock, and status bar
- Fake operator/system log panel
- Horizontal glitch sweeps and scan shimmer
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


class Column:
    def __init__(self, height: int):
        self.reset(height, fresh=True)

    def reset(self, height: int, fresh: bool = False) -> None:
        self.head_y = random.randint(-height, 0) if fresh else -random.randint(4, height // 2 + 8)
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

    def offscreen(self, height: int) -> bool:
        return self.head_y - self.length > height


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
        if now - self.last_update > random.uniform(0.35, 1.2):
            self.last_update = now
            msg = random.choice(LOG_MESSAGES)
            if random.random() < 0.22:
                msg += f" :: {random.randint(1000,9999):04X}"
            self.add(msg)


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


def draw_column(stdscr, x: int, col: Column, height: int, attrs) -> None:
    green_dim, green, green_bold, white_bold = attrs
    for i in range(col.length):
        y = col.head_y - i
        if y < 0:
            continue
        if y >= height:
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
    if 0 <= tail_y < height:
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


def maybe_draw_quit_hint(stdscr, width: int, height: int, attr) -> None:
    if width > 8 and height > 8 and random.random() < 0.012:
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        try:
            stdscr.addch(y, x, "Q", attr)
        except curses.error:
            pass


def maybe_glitch_sweep(stdscr, width: int, height: int, attrs) -> None:
    _, green, green_bold, white_bold = attrs
    if random.random() >= 0.018 or width < 12 or height < 5:
        return
    y = random.randint(1, height - 2)
    start = random.randint(0, max(0, width - 10))
    length = random.randint(8, min(34, width - start))
    for x in range(start, start + length):
        ch = random.choice(GLITCH + GLYPHS)
        attr = random.choice((green, green_bold, white_bold))
        try:
            stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass


def maybe_status_banner(stdscr, width: int, attrs) -> None:
    green_dim, green, green_bold, _ = attrs
    if random.random() >= 0.01 or width < 30:
        return
    text = f"[ {random.choice(STATUSES)} ]"
    x = max(1, (width - len(text)) // 2)
    attr = green_bold if random.random() < 0.4 else green_dim
    draw_text(stdscr, 1, x, text, attr)


def draw_hud(stdscr, attrs, status_text: str) -> None:
    green_dim, green, green_bold, _ = attrs
    h, w = stdscr.getmaxyx()

    draw_box(stdscr, 0, 0, h, w, green_dim)

    clock_text = time.strftime("%Y-%m-%d %H:%M:%S")
    draw_text(stdscr, 0, 2, " OPERATOR CONSOLE ", green_bold)
    draw_text(stdscr, 0, max(2, w - len(clock_text) - 2), clock_text, green)

    bottom = f" STATUS: {status_text} "
    quit_hint = " Q TO EXIT "
    draw_text(stdscr, h - 1, 2, bottom, green)
    draw_text(stdscr, h - 1, max(2, w - len(quit_hint) - 2), quit_hint, green_dim)


def draw_log_panel(stdscr, panel, attrs) -> None:
    green_dim, green, _, _ = attrs
    h, w = stdscr.getmaxyx()
    if h < 12 or w < 60:
        return

    pw = min(42, w // 3)
    ph = min(10, h - 4)
    top = 2
    left = 2

    draw_box(stdscr, top, left, ph, pw, green_dim)
    draw_text(stdscr, top, left + 2, " SYSTEM LOG ", green)

    visible = panel.lines[-(ph - 2):]
    for i, line in enumerate(visible, start=1):
        draw_text(stdscr, top + i, left + 1, line, green_dim if i < len(visible) else green)


def draw_scanlines(stdscr, attrs) -> None:
    green_dim, _, _, _ = attrs
    h, w = stdscr.getmaxyx()
    if random.random() < 0.65:
        for y in range(2, h - 1, 4):
            if random.random() < 0.25:
                x = random.randint(1, max(1, w - 8))
                draw_text(stdscr, y, x, random.choice(["....", "::", "..::..", "-----"]), green_dim)


def resize_columns(width: int, height: int):
    return [Column(height) for _ in range(width)]


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

    height, width = stdscr.getmaxyx()
    columns = resize_columns(width, height)
    panel = LogPanel(rows=8)
    for _ in range(5):
        panel.maybe_update()

    last_resize_check = time.monotonic()
    status_text = random.choice(STATUSES)
    last_status_change = 0.0

    while True:
        now = time.monotonic()

        if now - last_resize_check > 0.2:
            new_h, new_w = stdscr.getmaxyx()
            if (new_h, new_w) != (height, width):
                height, width = new_h, new_w
                stdscr.erase()
                columns = resize_columns(width, height)
            last_resize_check = now

        if now - last_status_change > random.uniform(3.5, 7.5):
            status_text = random.choice(STATUSES)
            last_status_change = now

        panel.maybe_update()

        for x, col in enumerate(columns):
            if not col.ready():
                continue
            col.advance()
            draw_column(stdscr, x, col, height - 1, attrs)
            if col.offscreen(height):
                col.reset(height)

        draw_scanlines(stdscr, attrs)
        maybe_glitch_sweep(stdscr, width, height, attrs)
        maybe_draw_quit_hint(stdscr, width, height, green_dim)
        maybe_status_banner(stdscr, width, attrs)

        if random.random() < 0.04 and width > 4 and height > 4:
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            try:
                stdscr.addch(y, x, random.choice(GLYPHS), white_bold if random.random() < 0.3 else green_bold)
            except curses.error:
                pass

        draw_log_panel(stdscr, panel, attrs)
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
