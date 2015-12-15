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
        self.cursor = Cursor(red)
        self.rendering_buffer = RenderingBuffer(red, cursor=self.cursor)
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
            key = self.ncurse_window.getch()

            if key != curses.KEY_RESIZE:
                self.handle_input(chr(key))

    def handle_input(self, key):
        if key == "j":
            self.cursor.go_down()
        elif key == "k":
            self.cursor.go_up()


class RenderingBuffer(object):
    def __init__(self, red, cursor):
        self.red = red
        self.buffer = red.dumps()
        self.cursor = cursor

    def get_window(self, size):
        height, width = size

        y1, x1, y2, x2 = self.cursor.get_cursor_square()

        to_return = []

        for line_number, i in enumerate(self.buffer.split("\n")):
            if line_number >= height:
                break

            if y1 <= line_number <= y2:
                # don't add a "\n" at the end of window, otherwise curses crash
                to_return.append((i[:width - 1] + ("\n" if line_number != height - 1 else ""), COLORS["selected"]))
            else:
                # don't add a "\n" at the end of window, otherwise curses crash
                to_return.append((i[:width - 1] + ("\n" if line_number != height - 1 else ""), COLORS["default"]))

        return to_return


class Cursor(object):
    def __init__(self, red):
        self.red = red
        self.current = red[0]

    def get_cursor_square(self):
        bounding_box = self.current.absolute_bounding_box

        left1, right1 = bounding_box.top_left.to_tuple()
        left2, right2 = bounding_box.bottom_right.to_tuple()
        return left1 - 1, right1 - 1, left2 - 1, right2 - 1

    def go_down(self):
        self.current = self.current.next

    def go_up(self):
        self.current = self.current.previous


def main(ncurse_window):
    init_colors()
    curses.curs_set(0)
    red = RedBaron(open(__file__, "r").read())
    Window(ncurse_window=ncurse_window, red=red).loop()


curses.wrapper(main)
