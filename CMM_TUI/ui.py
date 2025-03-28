import curses

class CMMUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.init_curses()
    
    def init_curses(self):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    
    def draw_position(self, position):
        """Draws the live position display at the top of the screen."""
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "CMM Control Panel", curses.color_pair(1))
        
        if position:
            self.stdscr.addstr(2, 0, f"Live Position - X: {position['X']:.2f}, Y: {position['Y']:.2f}, Z: {position['Z']:.2f}")
        else:
            self.stdscr.addstr(2, 0, "Live Position - Waiting for data...")
        
        self.stdscr.refresh()
    
    def draw_points(self, points):
        """Draws the measured points as a simple graph below the live position display."""
        h, w = self.stdscr.getmaxyx()
        
        for point in points:
            x = int((point['X'] / 100) * (w - 1))
            y = int((point['Y'] / 100) * (h - 4)) + 4  # Graph starts at row 4
            if 0 <= x < w and 4 <= y < h:
                self.stdscr.addch(y, x, '*')
        
        self.stdscr.refresh()
