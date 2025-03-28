import curses
import os

# Define constants
MENU_COLOR = 1
SELECTED_COLOR = 2

def list_dir(path):
    """ List directories and files in the given path. """
    try:
        entries = os.listdir(path)
        entries.sort(key=lambda e: (os.path.isdir(os.path.join(path, e)), e.lower()))
        return entries
    except PermissionError:
        return []

def print_menu(win, entries, selected_idx, current_path):
    win.clear()
    win.border()
    h, w = win.getmaxyx()

    # Display current directory path at the top
    win.addstr(1, 2, f"Current Directory: {current_path}", curses.color_pair(MENU_COLOR))

    # Display each entry in the list
    for idx, entry in enumerate(entries):
        x = 2
        y = idx + 3  # Offset by 3 for better visibility

        if y >= h - 1:  # Prevent text from running off the screen
            break

        if idx == selected_idx:
            win.attron(curses.color_pair(SELECTED_COLOR))
            win.addstr(y, x, entry)
            win.attroff(curses.color_pair(SELECTED_COLOR))
        else:
            win.addstr(y, x, entry)
    
    win.refresh()

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(MENU_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(SELECTED_COLOR, curses.COLOR_BLACK, curses.COLOR_CYAN)
    
    # Turn off cursor blinking
    curses.curs_set(0)
    
    # Get terminal size and create a new window
    h, w = stdscr.getmaxyx()
    win = curses.newwin(h - 2, w - 2, 1, 1)

    # Start browsing from the home directory
    current_path = os.path.expanduser("~")
    entries = list_dir(current_path)
    current_idx = 0

    print_menu(win, entries, current_idx, current_path)
    
    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_idx > 0:
            current_idx -= 1
        elif key == curses.KEY_DOWN and current_idx < len(entries) - 1:
            current_idx += 1
        elif key == ord('\n'):  # Enter key to open folders
            selected = entries[current_idx]
            selected_path = os.path.join(current_path, selected)
            
            if os.path.isdir(selected_path):
                # Navigate into the folder
                current_path = selected_path
                entries = list_dir(current_path)
                current_idx = 0
            elif os.path.isfile(selected_path):
                # Display file content (if it's a text file)
                try:
                    with open(selected_path, 'r') as file:
                        content = file.read()
                    
                    # Display file content in the window
                    win.clear()
                    win.border()
                    win.addstr(1, 1, f"Viewing {selected}", curses.color_pair(MENU_COLOR))
                    for i, line in enumerate(content.splitlines()):
                        if i + 3 >= h - 1:
                            break
                        win.addstr(i + 3, 1, line[:w - 2])
                    win.refresh()
                    
                    # Wait for user to press a key to go back
                    stdscr.getch()
                except Exception as e:
                    pass  # If file can't be opened, just ignore for now
        
        elif key == ord('q'):
            break

        print_menu(win, entries, current_idx, current_path)

# Run the program
curses.wrapper(main)
