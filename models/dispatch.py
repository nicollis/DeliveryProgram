import datetime

from models.status import Status
from models.flag import Flag


class Dispatch:
    def __init__(self, location, packages, addresses, address_indices, distances):
        self.hub = location
        self.packages = packages
        self.addresses = addresses
        self.address_indices = address_indices
        self.distances = distances

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def distanceBetween(self, address1, address2):
        address1_index = self.address_indices[address1]
        address2_index = self.address_indices[address2]
        return self.distances[address1_index][address2_index]

    # Time Complexity: O(N) where N is the number of packages in given truck
    # Space Complexity: O(1)
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
    # We use the lookup function to find the package with the flag WRONG_ADDRESS
    # This creates a large time and space complexity in the worst case.
    # However, we know in our case this would only return 1 package.
    # But to make this more "adaptable and scalable" I used the more complex lookup function
    # Time Complexity: O(N^k) where N is the number of addresses and K is the number of packages
    # Space Complexity: O(N) where N is the number of packages
    def updateAddress(self):
        packages = self.packages.lookup(flag=Flag.WRONG_ADDRESS)
        if package := packages[0]:
            package.address = '410 S State St'
            package.city = 'Salt Lake City'
            package.zip = '84111'
            package.status = Status.HUB
            self.packages[package.id] = package

    # Our function for loading packages onto our tucks and updating their status
    # Time Complexity: O(N) where N is the number of packages in given truck
    # Space Complexity: O(1)
    def loadTruckWithPackageList(self, forTruck, package_list):
        if len(package_list) > forTruck.package_capacity:
            raise Exception('Too many packages for truck')

        for package_id in package_list:
            package = self.packages[package_id]
            forTruck.loadPackage(package.id)
            package.status = Status.ENROUTE
            self.packages[package.id] = package

    # Our function for delivering packages at our current location
    # We build out our remaining packages to replace packages, due to an issue where
    # if you update the package list while looping though it packages can be skipped
    # due to shifting indexes
    # Time Complexity: O(N) where N is the number of packages in given truck
    # Space Complexity: O(N) where N is the number of delivered packages at the given address
    def truckDeliverAllPackagesAtCurrentLocation(self, forTruck):
        remaining_packages = []
        for package_id in forTruck.packages:
            package = self.packages[package_id]
            if package.address == forTruck.current_location:
                package.status = Status.DELIVERED
                package.delivery_time = forTruck.time.time()
                self.packages[package.id] = package
            else:
                remaining_packages.append(package_id)
        forTruck.packages = remaining_packages

    # Our main function for deliver packages and stopping if the user as requested a stop time
    # We loop until all packages are delivered from the truck
    # We deliver all packages at our current address
    # If we still have packages we use a greedy algorithm to find the closest address and travel there
    # Once we have delivered all packages we return to the hub
    # Time Complexity: O(n^2) where N is the number of packages
    # Space Complexity: O(1)
    def truckDeliverPackages(self, forTruck, end_time=None):
        while len(forTruck.packages) > 0: # Time Complexity: O(N) where N is the number of addresses we visit as we deliver packages by address not by package
            # deliver packages for this address
            self.truckDeliverAllPackagesAtCurrentLocation(forTruck) # Time Complexity: O(N) where N is the number of packages in given truck

            if len(forTruck.packages) == 0: break
            # find the next address and travel there
            next_address, distance = self.minDistanceFrom(forTruck.current_location, forTruck)
            if distance == float('inf'): break
            # drive the truck to the next address
            forTruck.drive(distance, next_address) # Time Complexity: O(1)
            # if the truck has passed the end time, stop
            if end_time is not None and forTruck.time.time() > end_time: break
        # send the truck home
        to_hub = self.distanceBetween(forTruck.current_location, self.hub) # O(1)
        forTruck.drive(to_hub, self.hub)

        return False if end_time is not None and forTruck.time.time() > end_time else True
