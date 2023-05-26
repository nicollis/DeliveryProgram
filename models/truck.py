import datetime


class Truck:
    def __init__(self, id, distance=0.0, time=0,
                 current_location=None, package_capacity=16,
                 truck_speed=18.0, start_time='8:00'
                 ):
        self.id = id
        self.packages = []
        self.distance = distance
        self.time = time
        self.current_location = current_location
        self.package_capacity = package_capacity
        self.truck_speed = truck_speed
        self.time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(start_time,
                                                                                                '%I:%M').time())

    def __str__(self):
        return f"Truck {self.id} ({self.current_location} {self.distance} {self.time.time()} {self.packages})"

    def loadPackage(self, package_id):
        if len(self.packages) < self.package_capacity:
            self.packages.append(package_id)
        else:
            raise Exception(f"Truck {self.id} is full. Cannot load package {package_id}")

    def timeAtArrival(self, distance):
        minutes_to_deliver = (distance / self.truck_speed) * 60
        return self.time + datetime.timedelta(minutes=minutes_to_deliver)

    def drive(self, distance, address):
        self.distance += distance
        self.time = self.timeAtArrival(distance)
        self.current_location = address
