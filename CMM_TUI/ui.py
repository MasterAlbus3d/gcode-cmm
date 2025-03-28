"""
User Interface Module

This module implements the ncurses TUI for interacting with the user.
"""

import curses

class UserInterface:
    def __init__(self, machine_controller):
        """
        Initialize the UserInterface.

        Args:
            machine_controller (MachineController): The machine controller instance.
        """
        self.machine_controller = machine_controller

    def run(self):
        """
        Starts the ncurses-based user interface.
        """
        curses.wrapper(self._main_loop)

    def _main_loop(self, stdscr):
        """
        The main loop running inside the curses wrapper.
        """
        # Clear screen
        stdscr.clear()
        stdscr.addstr(0, 0, "Welcome to the Machine Control Interface")
        stdscr.addstr(2, 0, "Press 'q' to quit.")
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
            # Further key handling and UI updates will be added here.
