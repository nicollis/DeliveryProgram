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
            # if package.deadline_as_time and \
            #     forTruck.timeAtArrival(distance) >= package.deadline_as_time - datetime.timedelta(minutes=60):
            #     return (package.address, distance)
        return min_address, min_distance

    def updateAddress(self):
        packages = self.packages.lookup(flag=Flag.WRONG_ADDRESS)
        if package := packages[0]:
            package.address = '410 S State St'
            package.city = 'Salt Lake City'
            package.zip = '84111'
            package.status = Status.HUB
            self.packages[package.id] = package

    # For early implementation we are not going to worry about
    # flags or anything special. We are just going to load the
    # packages in the order they are given to us.
    def truckLoadPackages(self, forTruck):
        # We know a packages address will update at '10:20 AM' we check if the truck looking at packages
        # is the truck that will be delivering the package. If it is we update the address.
        wait_until = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 20))
        if forTruck.time > wait_until: self.updateAddress()

        # Prioritize zipcode loading
        self.priorityNearbyAddresses(forTruck)

        # fill any additional space
        for package in self.packages.lookup(status=Status.HUB):
            if len(forTruck.packages) < forTruck.package_capacity:
                forTruck.loadPackage(package.id)
                package.status = Status.ENROUTE
                self.packages[package.id] = package

    def loadTruckWithPackageList(self, forTruck, package_list):
        if len(package_list) > forTruck.package_capacity:
            raise Exception('Too many packages for truck')

        for package_id in package_list:
            package = self.packages[package_id]
            forTruck.loadPackage(package.id)
            package.status = Status.ENROUTE
            self.packages[package.id] = package

    # look through packages already on the truck
    # check if there are any packages still at the Hub that are going to the same
    # nearby address as the packages on the truck
    def priorityNearbyAddresses(self, forTruck, delta=5):
        addresses = set()
        for package_id in forTruck.packages:
            package = self.packages[package_id]
            addresses.add(package.address)

        for address in addresses:
            for package in self.packages.lookup(status=Status.HUB):
                if self.distanceBetween(address, package.address) < delta and len(
                        forTruck.packages) < forTruck.package_capacity:
                    forTruck.loadPackage(package.id)
                    package.status = Status.ENROUTE
                    self.packages[package.id] = package

    def loadTruck1WithPriorityPackages(self, truck1):
        # first we want to make sure the grouped packages are all loaded together
        # we then want to load in any packages at the hub with a timed delivery by
        for package in {self.packages[13], self.packages[15], self.packages[19],
                        *self.packages.lookup(flag=Flag.DELIVER_WITH_OTHER_PACKAGES),
                        *self.packages.lookup(deadline='10:30 AM')}:
            if package.flag != Flag.DELAYED and len(truck1.packages) < truck1.package_capacity:
                truck1.loadPackage(package.id)
                package.status = Status.ENROUTE
                self.packages[package.id] = package

    def loadTruck2WithPriorityPackages(self, truck2):
        # we want to keep truck 2 around until 9:05 when the delayed packages arrive
        # if there is room on truck 2, we want to load the packages that are specific for it
        for package in [*self.packages.lookup(flag=Flag.DELAYED, deadline='10:30 AM'),
                        *self.packages.lookup(flag=Flag.ONLY_TRUCK_2),
                        *self.packages.lookup(status=Status.HUB)]:
            if len(truck2.packages) < truck2.package_capacity:
                truck2.loadPackage(package.id)
                package.status = Status.ENROUTE
                self.packages[package.id] = package

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

    def truckDeliverPackages(self, forTruck, end_time=None):
        while len(forTruck.packages) > 0:
            # deliver packages for this address
            self.truckDeliverAllPackagesAtCurrentLocation(forTruck)

            if len(forTruck.packages) == 0: break
            # find the next address and travel there
            next_address, distance = self.minDistanceFrom(forTruck.current_location, forTruck)
            if distance == float('inf'): break
            # drive the truck to the next address
            forTruck.drive(distance, next_address)
            # if the truck has passed the end time, stop
            if end_time is not None and forTruck.time.time() > end_time: break
        # send the truck home
        to_hub = self.distanceBetween(forTruck.current_location, self.hub)
        forTruck.drive(to_hub, self.hub)

        return False if end_time is not None and forTruck.time.time() > end_time else True
