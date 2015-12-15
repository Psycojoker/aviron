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
        for i in self.rendering_buffer.get_window(size=self.ncurse_window.getmaxyx()):
            if first:
                self.ncurse_window.addstr(0, 0, i)
                first = False
            else:
                self.ncurse_window.addstr(i)

        self.ncurse_window.refresh()

    def loop(self):
        while 42:
            self.render()
            self.ncurse_window.getch()


class RenderingBuffer(object):
    def __init__(self, red):
        self.red = red
        self.buffer = red.dumps()

    def get_window(self, size):
        height, width = size

        to_return = []

        for line_number, i in enumerate(self.buffer.split("\n")):
            if line_number >= height:
                break

            to_return.append(i[:width - 1] + "\n")

        return to_return


def main(ncurse_window):
    init_colors()
    curses.curs_set(0)
    red = RedBaron(open(__file__, "r").read())
    Window(ncurse_window=ncurse_window, red=red).loop()


curses.wrapper(main)
