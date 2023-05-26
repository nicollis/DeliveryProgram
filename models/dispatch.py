import datetime

from models.status import Status
from models.flag import Flag


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
            distance = self.distanceBetween(address, package.address)
            if distance != 0.0 and distance < min_distance:
                min_distance = distance
                min_address = package.address
        return min_address, min_distance

    # Our function for updating package #9 once the clock hits 10:20 AM
    def updateAddress(self):
        packages = self.packages.lookup(flag=Flag.WRONG_ADDRESS)
        if package := packages[0]:
            package.address = '410 S State St'
            package.city = 'Salt Lake City'
            package.zip = '84111'
            package.status = Status.HUB
            self.packages[package.id] = package

    # Our function for loading packages onto our tucks and updating their status
    # O(N) where N is the number of packages in given truck
    def loadTruckWithPackageList(self, forTruck, package_list):
        if len(package_list) > forTruck.package_capacity:
            raise Exception('Too many packages for truck')

        for package_id in package_list:
            package = self.packages[package_id]
            forTruck.loadPackage(package.id)
            package.status = Status.ENROUTE
            self.packages[package.id] = package

    # Our function for delivering packages at our current location
    # We have to loop through delivered packages twice due to a issue where
    # if you update the package list while looping though it packages can be skipped
    # due to shifting indexes
    # O(N) where N is the number of packages in given truck
    def truckDeliverAllPackagesAtCurrentLocation(self, forTruck):
        delivered = []
        for package_id in forTruck.packages:
            package = self.packages[package_id]
            if package.address == forTruck.current_location:
                package.status = Status.DELIVERED
                package.delivery_time = forTruck.time.time()
                delivered.append(package.id)
                self.packages[package.id] = package
        [forTruck.packages.remove(i) for i in delivered]

    # Our main function for deliver packages and stopping if the user as requested a stop time
    # We loop until all packages are delivered from the truck
    # We deliver all packages at our current address
    # If we still have packages we use a greedy algorithm to find the closest address and travel there
    # Once we have delivered all packages we return to the hub
    # O(n^k) where N is the number of addresses and K is the number of packages in given truck
    def truckDeliverPackages(self, forTruck, end_time=None):
        while len(forTruck.packages) > 0: # O(N) where N is the number of addresses we visit as we deliver packages by address not by package
            # deliver packages for this address
            self.truckDeliverAllPackagesAtCurrentLocation(forTruck) # O(N) where N is the number of packages in given truck

            if len(forTruck.packages) == 0: break
            # find the next address and travel there
            next_address, distance = self.minDistanceFrom(forTruck.current_location, forTruck) # O(N) where N is the number of packages in given truck
            if distance == float('inf'): break
            # drive the truck to the next address
            forTruck.drive(distance, next_address)
            # if the truck has passed the end time, stop
            if end_time is not None and forTruck.time.time() > end_time: break
        # send the truck home
        to_hub = self.distanceBetween(forTruck.current_location, self.hub)
        forTruck.drive(to_hub, self.hub)

        return False if end_time is not None and forTruck.time.time() > end_time else True
