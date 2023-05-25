from models.status import Status

class Dispatch:
    def __init__(self, location, packages, addresses, distances):
        self.hub = location
        self.packages = packages
        self.addresses = addresses
        self.distances = distances

    # O(N) where N is the number of addresses
    def distanceBetween(self, address1, address2):
        address1_index = self.addresses.index(address1)
        address2_index = self.addresses.index(address2)
        return self.distances[address1_index][address2_index]

    # O(N) where N is the number of packages in given truck
    def minDistanceFrom(self, address, forTruck):
        min_distance = float('inf')
        min_address = None
        for package_id in forTruck.packages:
            package = self.packages.get(package_id)
            if address == None: print('STOP', package)
            distance = self.distanceBetween(address, package.address)
            if distance != 0.0 and distance < min_distance:
                min_distance = distance
                min_address = package.address
        return (min_address, min_distance)
    
    # For early implementation we are not going to worry about
    # flags or anything special. We are just going to load the
    # packages in the order they are given to us.
    def truckLoadPackages(self, forTruck):
        for package in self.packages:
            if package.status == Status.HUB:
                if len(forTruck.packages) < forTruck.package_capacity:
                    forTruck.loadPackage(package.id)
                    package.status = Status.ENROUTE
                    self.packages[package.id] = package

    def truckDeliverAllPackagesAtCurrentLocation(self, forTruck):
        for package_id in forTruck.packages:
            package = self.packages[package_id]
            if package.address == forTruck.current_location:
                package.status = Status.DELIVERED
                package.delivery_time = forTruck.time.time()
                forTruck.packages.remove(package.id)
                self.packages[package.id] = package
    
    def truckDeliverPackages(self, forTruck):
        truck_history = {}
        while len(forTruck.packages) > 0:
          # deliver packages for this address
          self.truckDeliverAllPackagesAtCurrentLocation(forTruck)
          
          truck_history[forTruck.time.time()] = self.packages

          if len(forTruck.packages) == 0: break
          # find the next address and travel there
          next_address, distance = self.minDistanceFrom(forTruck.current_location, forTruck)
          if distance == float('inf'): break
          # drive the truck to the next address
          forTruck.drive(distance, next_address)
        # send the truck home
        to_hub = self.distanceBetween(forTruck.current_location, self.hub)
        forTruck.drive(to_hub, self.hub)

        return truck_history

    
