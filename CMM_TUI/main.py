"""
Main Module

This is the entry point of the application. It wires together the configuration,
serial communication, machine control, and user interface modules.
"""

from config import load_settings
from serial_comm import SerialComm
from machine import MachineController
from ui import UserInterface

def main():
    # Load settings
    settings = load_settings()

    # Setup serial communication
    serial_comm = SerialComm(settings["port"], settings["baud"])
    serial_comm.open()

    # Initialize machine controller
    machine_controller = MachineController(serial_comm)

    # Initialize and run the UI
    ui = UserInterface(machine_controller)
    ui.run()

if __name__ == "__main__":
    main()
