from package import Package

class Truck:
    def __init__(self, id, packages=[], distance=0.0, time=0, current_location = None):
        self.id = id
        self.packages = packages
        self.distance = distance
        self.time = time
        self.current_location = current_location