import curses
from redbaron import RedBaron


class Window(object):
    def __init__(self, ncurse_window, red):
        self.red = red
        self.ncurse_window = ncurse_window

    def render(self):
        self.ncurse_window.addstr(self.red.dumps())
        self.ncurse_window.refresh()
        self.ncurse_window.getch()


def main(ncurse_window):
    red = RedBaron(open(__file__, "r").read())
    Window(ncurse_window=ncurse_window, red=red).render()


curses.wrapper(main)
