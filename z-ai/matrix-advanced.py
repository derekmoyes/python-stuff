#!/usr/bin/env python3
"""
Deluxe Matrix-style terminal screensaver.

Controls:
    q / Q / Esc   Quit

Features:
- Half-width Katakana glyph rain
- Independent column speeds and trail lengths
- Startup title card and fade-in boot sequence
- Occasional horizontal glitch sweeps
- Subliminal quit hint ('Q') hidden in the stream
- Defensive curses handling for macOS / iTerm / Terminal.app
"""

import curses
import random
import time
import getpass  
import pwd

# Classic-feeling half-width Katakana plus digits and symbols.
GLYPHS = (
    "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ"
    "ﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓ"
    "ﾔﾕﾖﾗﾘﾙﾚﾛﾜ"
    "0123456789"
    "@#$%&*+=-:;<>?/|[]{}"
)

# Rare “glitch” characters mixed into the stream.
GLITCH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def get_first_name():
    try:
        gecos = pwd.getpwuid(0).pw_gecos
    except Exception:
        gecos = ""

    try:
        gecos = pwd.getpwuid(os.getuid()).pw_gecos
        name = gecos.split(",")[0].strip()
        if name:
            return name.split()[0]
    except Exception:
        pass

    # fallback
    return getpass.getuser().split()[0].capitalize()


def safe_curs_set(value: int) -> None:
    """Hide/show cursor without crashing on terminals that don't support it."""
    try:
        curses.curs_set(value)
    except curses.error:
        pass


def init_colors():
    """
    Initialize color pairs.

    Returns:
        (green_dim, green, green_bold, white_bold)
    Falls back to normal attributes if colors are unavailable.
    """
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
    """Represents one falling stream of glyphs."""

    def __init__(self, height: int):
        self.reset(height, fresh=True)

    def reset(self, height: int, fresh: bool = False) -> None:
        # Start either partially onscreen or just above the visible area.
        self.head_y = random.randint(-height, 0) if fresh else -random.randint(4, height // 2 + 6)
        self.speed = random.randint(1, 5)          # lower value = faster column
        self.length = random.randint(6, 22)
        self.tick = 0
        self.glyphs = [self.next_glyph() for _ in range(self.length)]

    def next_glyph(self) -> str:
        # Mostly classic glyphs, with rare glitch characters.
        return random.choice(GLYPHS if random.random() < 0.95 else GLITCH)

    def ready(self) -> bool:
        """Advance only on this column's own timing."""
        self.tick += 1
        if self.tick < self.speed:
            return False
        self.tick = 0
        return True

    def advance(self) -> None:
        """Move the head down one row and rotate the trail."""
        self.head_y += 1
        self.glyphs.insert(0, self.next_glyph())
        if len(self.glyphs) > self.length:
            self.glyphs.pop()

    def is_offscreen(self, height: int) -> bool:
        return self.head_y - self.length > height


def draw_column(stdscr, x: int, col: Column, height: int, attrs) -> None:
    """Draw one column with bright head and fading trail."""
    green_dim, green, green_bold, white_bold = attrs

    for i in range(col.length):
        y = col.head_y - i
        if y < 0:
            continue
        if y >= height:
            break

        # Occasional visible shimmer in the trail.
        if i > 0 and random.random() < 0.035:
            col.glyphs[i] = col.next_glyph()

        ch = col.glyphs[i]

        if i == 0:
            attr = white_bold                    # bright head
        elif i <= 2:
            attr = green_bold                    # near-head glow
        elif i < col.length * 0.55:
            attr = green                         # normal body
        else:
            attr = green_dim                     # dim tail

        try:
            stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass

    # Clear one cell beyond the tail for a crisp trailing edge.
    tail_y = col.head_y - col.length
    if 0 <= tail_y < height:
        try:
            stdscr.addch(tail_y, x, " ")
        except curses.error:
            pass


def boot_sequence(stdscr, attrs) -> None:
    """Show a short cinematic startup card."""
    green_dim, green, green_bold, white_bold = attrs
    h, w = stdscr.getmaxyx()

    name = get_first_name()
    intro_lines = [
        f"WAKE UP, {name.upper()}...",
        f"{name.upper()}, THE MATRIX HAS YOU...",
        f"HELLO, {name.upper()}...",
    ]
    title = random.choice(intro_lines)

    # title = f"WAKE UP, {name.upper()}..."
    # title = "WAKE UP, DEREK..."
    subtitle = "FOLLOW THE WHITE RABBIT"
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

    # Type-in effect.
    for row, (text, attr) in enumerate(lines):
        x0 = max(0, (w - len(text)) // 2)
        for i, ch in enumerate(text):
            try:
                stdscr.addch(start_y + row, x0 + i, ch, attr)
            except curses.error:
                pass
            stdscr.refresh()
            curses.napms(16)
        curses.napms(90)

    # Brief hold.
    end = time.monotonic() + 1.1
    while time.monotonic() < end:
        key = stdscr.getch()
        if key in (27, ord("q"), ord("Q")):
            raise KeyboardInterrupt
        curses.napms(20)

    # Scramble/glitch-out before rain starts.
    for _ in range(6):
        for row, (text, attr) in enumerate(lines):
            x0 = max(0, (w - len(text)) // 2)
            for i, ch in enumerate(text):
                shown = random.choice(GLITCH) if random.random() < 0.35 else ch
                try:
                    stdscr.addch(start_y + row, x0 + i, shown, attr)
                except curses.error:
                    pass
        stdscr.refresh()
        curses.napms(55)

    stdscr.erase()
    stdscr.refresh()


def maybe_draw_quit_hint(stdscr, width: int, height: int, attr) -> None:
    """
    Draw an occasional hidden 'Q' somewhere in the field.
    It should feel accidental rather than like a UI label.
    """
    if width > 6 and height > 6 and random.random() < 0.012:
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        try:
            stdscr.addch(y, x, "Q", attr)
        except curses.error:
            pass


def maybe_glitch_sweep(stdscr, width: int, height: int, attrs) -> None:
    """
    Rare horizontal glitch sweep across a single row.
    Short-lived, just enough to add cinematic texture.
    """
    _, green, green_bold, white_bold = attrs
    if random.random() >= 0.018 or width < 10 or height < 4:
        return

    y = random.randint(1, height - 2)
    start = random.randint(0, max(0, width - 8))
    length = random.randint(6, min(28, width - start))
    palette = (green, green_bold, white_bold)

    for x in range(start, start + length):
        ch = random.choice(GLITCH + GLYPHS)
        attr = random.choice(palette)
        try:
            stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass


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

    last_resize_check = time.monotonic()

    while True:
        now = time.monotonic()

        # Handle terminal resize periodically.
        if now - last_resize_check > 0.2:
            new_h, new_w = stdscr.getmaxyx()
            if (new_h, new_w) != (height, width):
                height, width = new_h, new_w
                stdscr.erase()
                columns = resize_columns(width, height)
            last_resize_check = now

        # Draw active columns.
        for x, col in enumerate(columns):
            if not col.ready():
                continue

            col.advance()
            draw_column(stdscr, x, col, height, attrs)

            if col.is_offscreen(height):
                col.reset(height)

        # Cinematic extras.
        maybe_glitch_sweep(stdscr, width, height, attrs)
        maybe_draw_quit_hint(stdscr, width, height, green_dim)

        # Very subtle random sparkle in the field.
        if random.random() < 0.05 and width > 2 and height > 2:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            try:
                stdscr.addch(y, x, random.choice(GLYPHS), white_bold if random.random() < 0.25 else green_bold)
            except curses.error:
                pass

        try:
            stdscr.refresh()
        except curses.error:
            pass

        key = stdscr.getch()
        if key in (27, ord("q"), ord("Q")):
            break

        # Master frame pacing.
        curses.napms(80)


if __name__ == "__main__":
    curses.wrapper(main)
