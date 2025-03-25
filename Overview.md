Overview
This Python script provides an interactive command‐line interface for controlling a machine (likely a CNC or coordinate measuring machine) via serial communication using G-code commands. The script reads configuration parameters (such as serial port, baud rate, grid settings, and output file) from a JSON settings file. It then opens a serial connection to the machine, sends a startup sequence, and offers two operational modes:

Rectangle Mode
– Performs an initial calibration for setting the starting position.
– Automatically generates a grid of measurement points based on the settings.
– Allows the user to adjust the Z-axis at each grid point and navigate between grid points interactively.
– Saves the measured data (machine positions) into a CSV file when all points are completed.

Free Mode
– Provides freeform manual control for moving the machine in X, Y, and Z axes using keyboard inputs.
– Allows the user to save individual points, undo points, and finally save the collected points to a CSV file.

The script uses raw keyboard input (via a custom getch() function) to capture user commands in real time and uses ANSI escape codes to style the terminal output.

Detailed Documentation by Section
1. Import Statements
Standard Libraries:
json for reading configuration files,
serial (from PySerial) for serial communication,
time for delays,
sys, termios, tty, and os for terminal and system operations,
csv for writing output data.

2. Function: read_settings()
Purpose:
Reads and parses the settings.json file to load configuration settings.

Returns:
A dictionary containing settings such as the serial port, baud rate, number of grid points, grid dimensions, and output filename.

3. Function: open_serial()
Purpose:
Opens a serial connection using the settings provided.

Actions:
Sends a wake-up sequence to the machine, waits briefly for the machine to initialize, and flushes any startup data from the serial buffer.

Returns:
An active serial connection object used to communicate with the machine.

4. Function: send_gcode(l)
Purpose:
Sends one or more G-code commands (provided as a multi-line string) over the serial connection.

Mechanism:
– Strips each line of any extraneous end-of-line characters.
– Appends a newline to each non-empty command and sends it over the serial port.
– Checks for and reads any responses from the machine.

5. Function: gotopoint()
Purpose:
Moves the machine to the next measurement point in the grid.

Mechanism:
– Lifts the machine to a preset Z height (from the starting position).
– Sends commands to move the machine to the specific X and Y coordinates of the current grid point.
– Updates the current position stored in the CMM class.

6. Function: getch()
Purpose:
Reads a single character from the terminal without waiting for the Enter key.

Mechanism:
Temporarily sets the terminal to raw mode to capture the keypress and then restores the terminal settings.

7. Class: CMM
Purpose:
Acts as a container for global parameters and state variables related to the measurement process.

Attributes:
– point: An index representing the current measurement point.
– point_list: A list of grid points (each being an [X, Y] coordinate pair).
– start: The starting position of the machine (an [X, Y, Z] coordinate).
– pos: The current position of the machine (an [X, Y, Z] coordinate).
– datapoints: A list to store the recorded machine positions (measurements).

8. Main Program Flow
Startup G-code:
Sends a startup sequence (e.g., homing all axes, turning off the part fan) to initialize the machine.

Mode Selection:
– Prompts the user to select between Rectangle (grid-based measurement) and Free (manual control) modes using key inputs ('z' for Rectangle, 'x' for Free).

Rectangle Mode:
Initial Calibration:
Allows the user to adjust the starting position using keyboard commands:

Z-axis adjustments: 'E' to raise, 'Q' to lower.

Y-axis adjustments: 'W' to move up, 'S' to move down.

X-axis adjustments: 'A' to move left, 'D' to move right.

Accept position: Press 'Y' when satisfied.

Grid Generation:
Uses the settings (number of points and distances) to compute a list of grid coordinates.

Interactive Measurement Loop:
Provides controls to:

Adjust the Z-axis with both larger (1mm) and finer (0.1mm) steps.

Navigate between grid points ('A' for previous, 'D' for next).

Save the current measurement at a grid point ('E') and automatically move to the next point.

Completion:
When all points have been measured, the collected data is saved to a CSV file. The machine is then returned to a safe home position.

Free Mode:
Interactive Controls:
Provides freeform movement in all three axes with different keys for different increments:

X-axis: 'D' (or 'L') for increasing, 'A' (or 'J') for decreasing.

Y-axis: 'W' (or 'I') for increasing, 'S' (or 'K') for decreasing.

Z-axis: 'E' (or 'O') for increasing, 'Q' (or 'U') for decreasing.

Point Management:

Save a point: Press 'P' to add the current position to the datapoints list.

Undo last point: Press 'Z' to remove the most recently saved point.

Save File: Press 'G' to write all saved points to the CSV file.

Exit Confirmation:
Both modes prompt for confirmation before quitting the program.