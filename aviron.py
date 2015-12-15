import curses
from redbaron import RedBaron

COLORS = {}


def init_colors():
    for number, (name, fg, bg) in enumerate((
           ("default", curses.COLOR_WHITE, curses.COLOR_BLACK),
           ("selected", curses.COLOR_BLACK, curses.COLOR_YELLOW),
        ), 1):
        curses.init_pair(number, fg, bg)
        COLORS[name] = curses.color_pair(number)


class Window(object):
    def __init__(self, ncurse_window, red):
        self.rendering_buffer = RenderingBuffer(red)
        self.ncurse_window = ncurse_window

    def render(self):
        first = True
        for i, color in self.rendering_buffer.get_window(size=self.ncurse_window.getmaxyx()):
            if first:
                self.ncurse_window.addstr(0, 0, i, color)
                first = False
            else:
                self.ncurse_window.addstr(i, color)

        self.ncurse_window.refresh()

    def loop(self):
        while 42:
            self.render()
            self.ncurse_window.getch()


class RenderingBuffer(object):
    def __init__(self, red):
        self.red = red
        self.buffer = red.dumps()
        self.cursor = Cursor(red)

    def get_window(self, size):
        height, width = size

        x1, y1, x2, y2 = self.cursor.get_cursor_square()

        to_return = []

        for line_number, i in enumerate(self.buffer.split("\n")):
            if line_number >= height:
                break

            # don't add a "\n" at the end of window, otherwise curses crash
            if line_number == height - 1:
                to_return.append((i[:width - 1], COLORS["default"]))
            else:
                to_return.append((i[:width - 1] + "\n", COLORS["default"]))

        return to_return


class Cursor(object):
    def __init__(self, red):
        self.red = red
        self.current = red[0]
        self.bounding_box = red[0].absolute_bounding_box

    def get_cursor_square(self):
        return map(lambda x: x - 1, self.bounding_box.top_left), map(lambda x: x - 1, self.bounding_box.bottom_right)


def main(ncurse_window):
    init_colors()
    curses.curs_set(0)
    red = RedBaron(open(__file__, "r").read())
    Window(ncurse_window=ncurse_window, red=red).loop()


curses.wrapper(main)
