class DataHandler:
    def __init__(self):
        self.points = []  # List of captured points (X, Y, Z)
    
    def record_point(self, position):
        """Records a point in memory."""
        if position:
            self.points.append(position)
    
    def get_points(self):
        """Returns all recorded points."""
        return self.points
    
    def save_to_file(self, filename="measurements.csv"):
        """Saves recorded points to a CSV file."""
        with open(filename, 'w') as file:
            file.write("X,Y,Z\n")
            for point in self.points:
                file.write(f"{point['X']},{point['Y']},{point['Z']}\n")
