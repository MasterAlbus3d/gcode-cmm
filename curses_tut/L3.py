import curses

def main(stdscr):
    # Initialize color support
    curses.start_color()
    
    # Define color pairs (foreground, background)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Clear screen
    stdscr.clear()

    # Get screen height and width
    h, w = stdscr.getmaxyx()
    
    # Create a new window
    win = curses.newwin(h - 2, w - 2, 1, 1)
    
    # Add a border to the window
    win.border()
    
    # Instructions
    stdscr.addstr(0, 0, "Press 'q' to Quit", curses.color_pair(1))
    stdscr.refresh()
    
    while True:
        win.clear()
        win.border()

        # Add some text to the window using colors
        win.addstr(1, 1, "Welcome to Python TUI Programming!", curses.color_pair(2))
        win.addstr(3, 1, "Use this window to build your UI.", curses.color_pair(3))
        
        # Refresh the window to render changes
        win.refresh()
        
        # Get user input
        key = stdscr.getch()
        
        if key == ord('q'):
            break

# Run the program
curses.wrapper(main)
import curses

def main(stdscr):
    # Initialize color support
    curses.start_color()
    
    # Define color pairs (foreground, background)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Clear screen
    stdscr.clear()

    # Get screen height and width
    h, w = stdscr.getmaxyx()
    
    # Create a new window
    win = curses.newwin(h - 2, w - 2, 1, 1)
    
    # Add a border to the window
    win.border()
    
    # Instructions
    stdscr.addstr(0, 0, "Press 'q' to Quit", curses.color_pair(1))
    stdscr.refresh()
    
    while True:
        win.clear()
        win.border()

        # Add some text to the window using colors
        win.addstr(1, 1, "Welcome to Python TUI Programming!", curses.color_pair(2))
        win.addstr(3, 1, "Use this window to build your UI.", curses.color_pair(3))
        
        # Refresh the window to render changes
        win.refresh()
        
        # Get user input
        key = stdscr.getch()
        
        if key == ord('q'):
            break

# Run the program
curses.wrapper(main)
