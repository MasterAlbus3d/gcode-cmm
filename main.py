import curses
from ui import CMMUI
from data_handler import DataHandler
from serial_communication import CMMCommunicator
import time

def main(stdscr):
    cmm_ui = CMMUI(stdscr)
    data_handler = DataHandler()
    communicator = CMMCommunicator(port='/dev/ttyUSB0')
    
    while True:
        position = communicator.get_position()
        
        if position:
            cmm_ui.draw_position(position)
        
        # Record point if the user presses 'r'
        key = stdscr.getch()
        if key == ord('r'):
            data_handler.record_point(position)
        
        # Quit the program if the user presses 'q'
        if key == ord('q'):
            communicator.close()
            break
        
        # Display points as a simple plot
        cmm_ui.draw_points(data_handler.get_points())
        
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
