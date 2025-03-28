import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Print Hello World at row 0, column 0
    stdscr.addstr(0, 0, "Hello, World!")
    
    # Refresh the screen to show the changes
    stdscr.refresh()
    
    # Wait for user to press any key
    stdscr.getch()

# Start the curses application
curses.wrapper(main)
