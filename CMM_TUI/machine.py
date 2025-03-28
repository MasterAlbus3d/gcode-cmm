"""
Machine Control Module

This module defines the MachineController class which handles G-code
commands, movement, and querying the machine position.
"""

import time
from serial_comm import SerialComm

class MachineController:
    def __init__(self, serial_comm):
        """
        Initialize the MachineController.

        Args:
            serial_comm (SerialComm): An instance of the SerialComm class.
        """
        self.serial_comm = serial_comm
        self.position = [0.0, 0.0, 0.0]  # Current position [X, Y, Z]
        self.grid_points = []           # List of grid points (if applicable)

    def send_gcode(self, command):
        """
        Sends a G-code command using the serial communication module.

        Args:
            command (str): G-code command.
        """
        self.serial_comm.send(command)
        # Optionally, you can read and handle the response here.
        time.sleep(0.1)

    def query_position(self):
        """
        Queries the machine for its current position using M114.

        Returns:
            list: The current [X, Y, Z] coordinates.
        """
        self.serial_comm.send("M114")
        time.sleep(0.1)
        response = self.serial_comm.read_response()
        # Parse the response string to extract coordinates (implementation needed)
        # For now, we'll assume the format is "X:10.00 Y:20.00 Z:30.00"
        coords = {}
        for part in response.split():
            if ":" in part:
                key, value = part.split(":", 1)
                if key in ("X", "Y", "Z"):
                    try:
                        coords[key] = float(value)
                    except ValueError:
                        coords[key] = 0.0
        self.position = [
            coords.get("X", 0.0),
            coords.get("Y", 0.0),
            coords.get("Z", 0.0)
        ]
        return self.position

    def move_to(self, x, y, z):
        """
        Moves the machine to the specified coordinates.

        Args:
            x (float): Target X coordinate.
            y (float): Target Y coordinate.
            z (float): Target Z coordinate.
        """
        self.send_gcode(f"G0 X{x} Y{y} Z{z}")
        # Update internal position by querying the machine after moving
        return self.query_position()

    def run_calibration(self):
        """
        Runs the calibration routine.
        """
        # Implementation of calibration logic goes here.
        pass
