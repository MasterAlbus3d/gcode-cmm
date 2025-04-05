class Config:
    def __init__(self):
        # Default settings
        self.settings = {
            "port": "/dev/ttyUSB0",
            "baudrate": 115200,
            "timeout": 1,
            "simulation_mode": True,
            "points_x": 5,
            "points_y": 5,
            "dist_x": 100,
            "dist_y": 100,
            "measurement_save_path": "measurements.csv"
        }
    
    def get(self, key):
        return self.settings.get(key)
    
    def set(self, key, value):
        if key in self.settings:
            self.settings[key] = value

    def get_all(self):
        return self.settings
