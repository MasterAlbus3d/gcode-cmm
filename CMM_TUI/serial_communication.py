import serial
import time

class CMMCommunicator:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        
    def get_position(self):
        """Sends the M114 command to get the current position."""
        try:
            self.ser.write(b'M114\n')
            time.sleep(0.1)
            response = self.ser.readline().decode().strip()
            
            # Example response: "X:10.00 Y:20.00 Z:30.00 E:0.00"
            if response.startswith("X:"):
                return self.parse_position(response)
            return None
        except Exception as e:
            return None
    
    def parse_position(self, response):
        """Parses the response from M114 to extract X, Y, Z positions."""
        try:
            parts = response.split(" ")
            position = {}
            for part in parts:
                if ':' in part:
                    axis, value = part.split(':')
                    if axis in "XYZ":
                        position[axis] = float(value)
            return position
        except:
            return None
    
    def close(self):
        self.ser.close()
