#!/usr/bin/env python3
"""
Coordinate Measurement Machine (CMM) Control Script

This script connects to a machine via a serial interface, sends G-code commands,
and allows the user to interactively calibrate and record measurement points.

Key functionalities include:
    - Reading configuration settings from a JSON file.
    - Establishing a serial connection to the machine.
    - Sending G-code commands and reading responses.
    - Tracking the machine's position via internal state (and potentially querying
      actual coordinates with M114 in the future).
    - Two modes of operation:
         * "Rectangle" mode: automatically generates a grid and records positions.
         * "Free" mode: allows manual control and point collection.
    - Using ANSI escape codes for styled terminal output.
"""
import json
import serial
import time
import sys
import termios
import tty
import os
import csv

def query_current_position():
    """
    Queries the machine for its current coordinates using M114.
    Assumes the machine's axes have been homed.
    
    Returns:
        list: A list containing [X, Y, Z] coordinates.
    """
    # Send M114 command to query the position.
    s.write("M114\n".encode())
    time.sleep(0.1)  # Allow time for the machine to respond

    # Read the response from the serial port.
    # Depending on your firmware, you might need to read multiple lines.
    response = s.readline().decode().strip()

    # Parse the response, expecting a format like: "X:10.00 Y:20.00 Z:30.00 E:0.00 ..."
    coords = {}
    for part in response.split():
        if ":" in part:
            key, value = part.split(":", 1)
            if key in ("X", "Y", "Z"):
                try:
                    coords[key] = float(value)
                except ValueError:
                    coords[key] = 0.0
    # Return the X, Y, Z coordinates, defaulting to 0 if not found.
    return [coords.get("X", 0.0), coords.get("Y", 0.0), coords.get("Z", 0.0)]

def read_settings():
    """
    Reads the settings from 'settings.json' and returns them as a dictionary.
    
    Expected JSON keys:
      - port: Serial port to connect (e.g., "/dev/ttyUSB0" or "COM3")
      - baud: Baud rate for serial communication (e.g., 115200)
      - points_x: Number of measurement points along the X-axis
      - points_y: Number of measurement points along the Y-axis
      - dist_x: Distance to cover along the X-axis
      - dist_y: Distance to cover along the Y-axis
      - output_file: Filename to save the measurement data (CSV format)
    """
    with open("settings.json") as settings_json:
        settings = json.load(settings_json)
        return settings

def open_serial():
    """
    Opens a serial connection using settings read from 'settings.json'.
    
    Actions:
      - Prints a message indicating the attempt to connect.
      - Sends a wake-up command to the device.
      - Waits for the device to initialize.
      - Flushes any startup text from the serial input buffer.
    
    Returns:
      An open serial connection object.
    """
    print("Connecting to serial...")
    s = serial.Serial(settings["port"], settings["baud"])

    # Send wake-up command to the serial device.
    s.write("\r\n\r\n".encode())
    time.sleep(2)   # Wait for initial device initialization
    s.flushInput()  # Flush any startup text from the buffer
    return s

def send_gcode(l):
    """
    Sends one or more G-code commands to the machine over the serial connection.
    
    Parameters:
      l (str): A string that may contain multiple lines of G-code.
      
    For each non-empty line:
      - Strips end-of-line characters.
      - Appends a newline character.
      - Writes the command to the serial port.
      - Reads and discards any immediate response from the device.
    """
    l = l.strip()  # Remove extraneous whitespace or EOL characters

    for line in l.splitlines():
        if not line.isspace() and len(line) > 0:
            line = line + "\n"
            s.write(line.encode())  # Send the G-code command
            # Read any responses available in the serial buffer
            while s.inWaiting() > 0:
                response = s.readline().decode().strip()

def gotopoint():
    """
    Moves the machine to the current measurement point defined in the CMM class.
    
    Actions:
      - Lifts the tool head to the starting Z position.
      - Retrieves the current grid point from CMM.point_list.
      - Moves the tool head to the specified X and Y coordinates.
      - Updates the current position stored in CMM.pos.
    """
    # Move to starting Z position before moving in X and Y
    send_gcode(f"G0Z{CMM.start[2]}")
    
    # Get current measurement point from the grid
    point = CMM.point_list[CMM.point]
    
    # Move to the target X and Y coordinates
    send_gcode(f"G0X{point[0]}Y{point[1]}")
    
    # Update current position with new X, Y and starting Z (unchanged)
    CMM.pos = [point[0], point[1], CMM.start[2]]

def getch():
    """
    Captures a single character from standard input without the need for the Enter key.
    
    This function temporarily sets the terminal to raw mode, reads one character, 
    and then restores the terminal's original settings.
    
    Returns:
      A single character input from the user.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class CMM:
    """
    Class to hold state information for the coordinate measurement process.
    
    Attributes:
      point (int): Index of the current measurement point in the grid.
      point_list (list): List of grid points; each point is a list [X, Y].
      start (list): Starting position as [X, Y, Z].
      pos (list): Current machine position as [X, Y, Z].
      datapoints (list): List for storing measurement data (positions).
    """
    point = 0  # Current index in the grid
    point_list = []  # List to store all generated grid points

    start = [0, 0, 0]  # Starting position [X, Y, Z]
    pos = [0, 0, 0]    # Current position [X, Y, Z]

    datapoints = []    # List to save measured datapoints

# Startup G-code commands sent to initialize the machine.
startup_gcode = """
M107 P1 ; Turn off part fan
G28 ; Home all axes
; G1 Z50 F5000 ; Move Z Axis up to allow attachment of CMM
"""

# Read settings from JSON file and open the serial connection.
settings = read_settings()
s = open_serial()

# Send the startup G-code sequence.
print("Sending startup GCODE")
send_gcode(startup_gcode)
# Uncomment the next line if you want to preset the Z axis position.
# CMM.pos[2] = 50

# Mode selection prompt.
print(f"\033[1mMODE SELECTION\033[0m")
print(f"\033[95m\033[1mZ\033[0m: Rectangle    \033[95m\033[1mX\033[0m: Free")

# Wait for user to select a mode by pressing 'z' (Rectangle) or 'x' (Free).
while True:
    char = getch()
    if char == "z":
        mode = "Rectangle"
        break
    if char == "x":
        mode = "Free"
        break

if mode == "Rectangle":
    # --- RECTANGLE MODE: Grid-based Measurement ---
    print(f"\033[1mINITIAL CALIBRATION\033[0m")
    print(
        f"\033[95m\033[1mX\033[0m: Exit    \033[95m\033[1mE\033[0m: Z Up    "
        f"\033[95m\033[1mQ\033[0m: Z Down    \033[95m\033[1mW\033[0m: Y Up    "
        f"\033[95m\033[1mS\033[0m: Y Down\033[0m    \033[95m\033[1mA\033[0m: X Up    "
        f"\033[95m\033[1mD\033[0m: X Down    \033[95m\033[1mY\033[0m: Accept Start Position\033[0m"
    )

    # Calibration loop: Adjust starting position until the user accepts it.
    while True:
        char = getch()
        if char == "x":
            exit(0)
        if char == "e":
            # Increase Z by 1mm.
            CMM.pos[2] += 1
            send_gcode("G0Z" + str(CMM.pos[2]))
        if char == "q":
            # Decrease Z by 1mm.
            CMM.pos[2] -= 1
            send_gcode("G0Z" + str(CMM.pos[2]))
        elif char == "w":
            # Increase Y by 5mm.
            CMM.pos[1] += 5
            send_gcode("G0Y" + str(CMM.pos[1]))
        elif char == "s":
            # Decrease Y by 5mm.
            CMM.pos[1] -= 5
            send_gcode("G0Y" + str(CMM.pos[1]))
        elif char == "a":
            # Increase X by 5mm (moving left on the screen).
            CMM.pos[0] -= 5
            send_gcode("G0X" + str(CMM.pos[0]))
        elif char == "d":
            # Decrease X by 5mm (moving right on the screen).
            CMM.pos[0] += 5
            send_gcode("G0X" + str(CMM.pos[0]))
        elif char == "y":
            # Accept the current position as the starting position.
            print("Accepted position")
            CMM.start = CMM.pos
            break

    # Generate grid points based on settings.
    for x in range(settings["points_x"]):
        pos_x = CMM.start[0] + x / (settings["points_x"] - 1) * settings["dist_x"]
        for y in range(settings["points_y"]):
            pos_y = CMM.start[1] + y / (settings["points_y"] - 1) * settings["dist_y"]
            CMM.point_list.append([pos_x, pos_y])

    # Initialise the datapoints list with the same number of elements as grid points.
    print("Initialising datapoints list...")
    CMM.datapoints = [0] * len(CMM.point_list)

    # Move to the first grid point.
    gotopoint()

    print(
        f"\r[{CMM.point}]  \033[95m\033[1mX\033[0m: Quit    "
        f"\033[95m\033[1mW/I\033[0m: Z Up    \033[95m\033[1mS/K\033[0m: Z Down    "
        f"\033[95m\033[1mD\033[0m: Next Grid Point    \033[95m\033[1mA\033[0m: Previous Grid Point    "
        f"\033[95m\033[1mE\033[0m: Save & Next Grid Point\033[0m"
    )

    # Main loop for grid measurement.
    while True:
        char = getch()
        if char == "x":
            print("Are you sure you want to quit? [y/n]: ", end="", flush=True)
            while True:
                char = getch()
                if char.lower() == "y":
                    exit(0)
                elif char.lower() == "n":
                    print("Not exiting...")
                    break
                else:
                    print("Please input y or n: ", end="", flush=True)

        if char == "w":
            # Increase Z by 1mm.
            CMM.pos[2] += 1
            send_gcode("G0Z" + str(CMM.pos[2]))
        elif char == "s":
            # Decrease Z by 1mm.
            CMM.pos[2] -= 1
            send_gcode("G0Z" + str(CMM.pos[2]))
        if char == "i":
            # Increase Z by a fine step (0.1mm).
            CMM.pos[2] += 0.1
            send_gcode("G0Z" + str(CMM.pos[2]))
        elif char == "k":
            # Decrease Z by a fine step (0.1mm).
            CMM.pos[2] -= 0.1
            send_gcode("G0Z" + str(CMM.pos[2]))
        elif char == "a":
            # Navigate to the previous grid point if available.
            if CMM.point > 0:
                CMM.point -= 1
                gotopoint()
        elif char == "d":
            # Navigate to the next grid point if available.
            if CMM.point < len(CMM.point_list) - 1:
                CMM.point += 1
                gotopoint()
        elif char == "e":
            # Save the current measurement (position) for the current grid point.
            CMM.datapoints[CMM.point] = CMM.pos
            if CMM.point < len(CMM.point_list) - 1:
                CMM.point += 1
                gotopoint()
            else:
                # All grid points have been measured.
                print("All points complete! Saving to file...")
                print(CMM.datapoints)
                with open(settings["output_file"], "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(CMM.datapoints)
                # Return machine to home position.
                send_gcode(f"G0Z{CMM.start[2]}")
                send_gcode(f"G0X0Y0")
                send_gcode(f"G0Z0")
                exit(0)

elif mode == "Free":
    # --- FREE MODE: Manual Control ---
    print(
        f"\033[95m\033[1mX\033[0m: Quit    "
        f"\033[95m\033[1mW/I\033[0m: Y Up    \033[95m\033[1mS/K\033[0m: Y Down    "
        f"\033[95m\033[1mD/L\033[0m: X Up    \033[95m\033[1mA/J\033[0m: X Down    "
        f"\033[95m\033[1mE/O\033[0m: Z Up    \033[95m\033[1mQ/U\033[0m: Z Down    "
        f"\033[95m\033[1mP\033[0m: Save Point    \033[95m\033[1mZ\033[0m: Undo Point    "
        f"\033[95m\033[1mG\033[0m: Save File"
    )

    # Main loop for free mode control.
    while True:
        char = getch()
        if char == "x":
            print("Are you sure you want to quit? [y/n]: ", end="", flush=True)
            while True:
                char = getch()
                if char.lower() == "y":
                    exit(0)
                elif char.lower() == "n":
                    print("Not exiting...")
                    break
                else:
                    print("Please input y or n: ", end="", flush=True)
        
        # --- X-axis control ---
        if char == "d" or char == "l":
            # Increase X (move right) by 1mm or 0.1mm depending on key.
            inc = 1 if char == "d" else 0.1
            CMM.pos[0] += inc
            send_gcode("G0X" + str(CMM.pos[0]))
        if char == "a" or char == "j":
            # Decrease X (move left) by 1mm or 0.1mm.
            inc = 1 if char == "a" else 0.1
            CMM.pos[0] -= inc
            send_gcode("G0X" + str(CMM.pos[0]))
        
        # --- Y-axis control ---
        if char == "w" or char == "i":
            # Increase Y (move up) by 1mm or 0.1mm.
            inc = 1 if char == "w" else 0.1
            CMM.pos[1] += inc
            send_gcode("G0Y" + str(CMM.pos[1]))
        if char == "s" or char == "k":
            # Decrease Y (move down) by 1mm or 0.1mm.
            inc = 1 if char == "s" else 0.1
            CMM.pos[1] -= inc
            send_gcode("G0Y" + str(CMM.pos[1]))
        
        # --- Z-axis control ---
        if char == "e" or char == "o":
            # Increase Z by 1mm or 0.1mm.
            inc = 1 if char == "e" else 0.1
            CMM.pos[2] += inc
            send_gcode("G0Z" + str(CMM.pos[2]))
        if char == "q" or char == "u":
            # Decrease Z by 1mm or 0.1mm.
            inc = 1 if char == "q" else 0.1
            CMM.pos[2] -= inc
            send_gcode("G0Z" + str(CMM.pos[2]))
        
        # --- Datapoint management ---
        if char == "p":
            # Save the current position as a datapoint.
            CMM.datapoints.append(list(CMM.pos))
        if char == "z":
            # Undo the last saved datapoint.
            CMM.datapoints.pop()
        if char == "g":
            # Save all collected datapoints to the output CSV file.
            with open(settings["output_file"], "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(CMM.datapoints)
