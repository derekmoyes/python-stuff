#!/usr/bin/env python3
import curses, random

#CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#$%&*+=-:."
CHARS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜ0123456789@#$%&*+=-:."

def main(stdscr):
    try: curses.curs_set(0)
    except curses.error: pass
    stdscr.nodelay(True)

    if curses.has_colors():
        try:
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_WHITE, -1)
            green, white = curses.color_pair(1), curses.color_pair(2) | curses.A_BOLD
        except curses.error:
            green = white = 0
    else:
        green = white = 0

    h, w = stdscr.getmaxyx()
    drops = [random.randrange(-h, h) for _ in range(w)]

    while True:
        for x in range(w):
            y = drops[x]
            for i, attr in ((0, white), (1, green), (2, green), (3, green)):
                yy = y - i
                if 0 <= yy < h:
                    try: stdscr.addch(yy, x, random.choice(CHARS), attr)
                    except curses.error: pass
            if 0 <= y - 4 < h:
                try: stdscr.addch(y - 4, x, " ")
                except curses.error: pass
            speed = [random.randint(1, 3) for _ in range(w)]
#            drops[x] = -random.randint(1, 20) if y > h else y + 1
            drops[x] = -random.randint(1, 20) if y > h else y + (1 if random.randint(1, 3) <= speed[x] else 0)

        stdscr.refresh()
        if stdscr.getch() in (27, ord("q")):
            break
        curses.napms(80)

if __name__ == "__main__":
    curses.wrapper(main)
