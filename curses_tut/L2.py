import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Turn off cursor blinking
    curses.curs_set(0)
    
    # Get screen dimensions
    h, w = stdscr.getmaxyx()

    # Initial position of the cursor
    x, y = w // 2, h // 2

    # Display instructions
    stdscr.addstr(0, 0, "Use arrow keys to move, Press 'q' to quit.")

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Use arrow keys to move, Press 'q' to quit.")

        # Draw the cursor at the current position
        stdscr.addstr(y, x, '@')

        # Refresh the screen
        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        # Handle user input
        if key == ord('q'):
            break  # Exit the loop when 'q' is pressed
        elif key == curses.KEY_UP and y > 1:
            y -= 1
        elif key == curses.KEY_DOWN and y < h - 1:
            y += 1
        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < w - 1:
            x += 1

# Run the program
curses.wrapper(main)
