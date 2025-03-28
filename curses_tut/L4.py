import curses

menu = ['Home', 'View Files', 'Settings', 'Help', 'Exit']

def print_menu(win, selected_idx):
    win.clear()
    win.border()
    
    h, w = win.getmaxyx()
    
    for idx, item in enumerate(menu):
        x = w//2 - len(item)//2
        y = h//2 - len(menu)//2 + idx
        
        if idx == selected_idx:
            # Highlight the selected item
            win.attron(curses.color_pair(1))
            win.addstr(y, x, item)
            win.attroff(curses.color_pair(1))
        else:
            win.addstr(y, x, item)
    
    win.refresh()

def main(stdscr):
    # Initialize color support
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    
    # Turn off cursor blinking
    curses.curs_set(0)

    # Create a new window
    h, w = stdscr.getmaxyx()
    win = curses.newwin(h - 2, w - 2, 1, 1)
    
    current_idx = 0
    print_menu(win, current_idx)
    
    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_idx > 0:
            current_idx -= 1
        elif key == curses.KEY_DOWN and current_idx < len(menu) - 1:
            current_idx += 1
        elif key == ord('\n'):  # Enter key
            if menu[current_idx] == 'Exit':
                break  # Quit the app
            else:
                # Display a message about the selected item
                win.clear()
                win.border()
                win.addstr(1, 1, f"You selected '{menu[current_idx]}'! Press any key to go back.")
                win.refresh()
                stdscr.getch()  # Wait for user to press a key
                
        # Refresh the menu display
        print_menu(win, current_idx)

# Run the program
curses.wrapper(main)
