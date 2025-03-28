"""
Serial Communication Module

This module manages the serial port connection and data transfer.
"""

import serial
import time

class SerialComm:
    def __init__(self, port, baud):
        """
        Initialize the serial communication.

        Args:
            port (str): Serial port (e.g., "/dev/ttyUSB0" or "COM3").
            baud (int): Baud rate (e.g., 115200).
        """
        self.port = port
        self.baud = baud
        self.ser = None

    def open(self):
        """Opens the serial connection and initializes the device."""
        print("Connecting to serial port...")
        self.ser = serial.Serial(self.port, self.baud)
        # Wake up the device
        self.ser.write("\r\n\r\n".encode())
        time.sleep(2)
        self.ser.flushInput()

    def send(self, command):
        """
        Sends a command over the serial port.

        Args:
            command (str): G-code command to send.
        """
        if self.ser is None:
            raise Exception("Serial connection not open.")
        self.ser.write(f"{command}\n".encode())

    def read_response(self):
        """
        Reads a response from the serial port.

        Returns:
            str: The response from the device.
        """
        if self.ser is None:
            raise Exception("Serial connection not open.")
        # You may want to read until a certain terminator is reached.
        return self.ser.readline().decode().strip()
