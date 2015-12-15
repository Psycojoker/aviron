import curses
from redbaron import RedBaron


class Window(object):
    def __init__(self, ncurse_window, red):
        self.rendering_buffer = RenderingBuffer(red)
        self.ncurse_window = ncurse_window

    def render(self):
        self.ncurse_window.addstr(0, 0, self.rendering_buffer.get_window(size=self.ncurse_window.getmaxyx()))
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

            to_return.append(i[:width - 1])

        return "\n".join(to_return)


def main(ncurse_window):
    curses.curs_set(0)
    red = RedBaron(open(__file__, "r").read())
    Window(ncurse_window=ncurse_window, red=red).loop()


curses.wrapper(main)
