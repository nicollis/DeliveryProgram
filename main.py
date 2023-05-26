# Author: Nicholas Ollis
# Student ID: #011097828
import csv
import datetime

from algorithms.hashtable import HashTable
from models.package import Package
from models.truck import Truck
from models.dispatch import Dispatch


# read data from package.csv and load into our hash table
# Time Complexity: O(n) where n is the number of packages
# Space Complexity: O(n) where n is the number of packages
def load_page_data():
    packages = HashTable()
    with open('data/packages.csv') as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
        for row in reader:
            try:
                package = Package(int(row[0]), row[1], row[2], int(row[4]), row[5], int(row[6]),
                                  row[7])  # todo: classify flags
                packages.append(package.id, package)
            except ValueError as e:
                print(f"Problem loading the package with id: {row[0]} into the hash table.\n {e}")
    return packages

# reads data from distances.csv and loads into a list of addresses and a list of distances.
# distance is a multidimensional list where the first index is the address and the second index
# is the other address we want the distance too.
# Time Complexity: O(n) where n is the number of addresses
# Space Complexity: O(n^2) where n is the number of addresses
def load_distance_data():
    addresses = []
    distances = []
    with open('data/distances.csv') as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
        for row in reader:
            row[0] = row[0].split('\n')[1].strip()
            addresses.append(row[0])
            distances.append([float(dist) for dist in row[2:]])

    return (addresses, distances)

# Our main function for delivering packages
# Time Complexity: O(n^k) where n is the number of addresses and k is the number of packages
# Due to use avoid loops in this function, we condense the time complexity to O(n^k) as it is the most expensive
# Space Complexity: O(P+A^2) where P is the number of packages, A is the number of addresses
def deliver(end_time=None):
    # Load in the packages
    packages = load_page_data() # Time Complexity: O(n) where n is the number of packages
    # Load in the distances
    addresses, distances = load_distance_data() # Time Complexity: O(n) where n is the number of addresses

    HUB = addresses[0]  # the hub is the first address in the list

    truck1_package_logs = [
        [13, 14, 15, 16, 19, 20, 39, 21, 34, 7, 29, 27, 35, 37, 30, 8],
        [24, 22, 18, 11, 23, 12]
    ]

    truck2_package_logs = [
        [25, 26, 6, 28, 31, 32, 1, 4, 40, 17, 36],
        [10, 5, 38, 3, 9, 2, 33]
    ]

    # if end_time is before 9:05 am, then we avoid loading truck 2 as it will not be used
    load_truck2 = True if end_time == None or datetime.datetime.combine(datetime.date.today(), end_time) >= \
                          datetime.datetime.combine(datetime.date.today(),
                                                    datetime.datetime.strptime('9:05 am', '%I:%M %p').time()) else False

    # Create our trucks and dispatch
    truck1 = Truck(1, current_location=HUB)
    truck2 = Truck(2, current_location=HUB, start_time='9:05')
    dispatch = Dispatch(HUB, packages, addresses, distances)

    # Load the trucks with the packages
    dispatch.loadTruckWithPackageList(truck1, truck1_package_logs[0]) # Time Complexity: O(n) where n is the number of packages
    if load_truck2:
        dispatch.loadTruckWithPackageList(truck2, truck2_package_logs[0])   # Time Complexity: O(n) where n is the number of packages

    # Deliver the packages
    success1 = dispatch.truckDeliverPackages(truck1, end_time)  # Time Complexity: O(n^k) where n is the number of addresses and k is the number of packages
    success2 = dispatch.truckDeliverPackages(truck2, end_time)  # Time Complexity: O(n^k) where n is the number of addresses and k is the number of packages

    # This is our logic check if we have hit the end time request by the user and need to return the program early
    if not success1 or not success2:
        return (dispatch, truck1, truck2)

    # Load the second set of packages and update the address of package 9
    dispatch.loadTruckWithPackageList(truck1, truck1_package_logs[1]) # Time Complexity: O(n) where n is the number of packages
    dispatch.updateAddress() # Time Complexity: O(1)
    dispatch.loadTruckWithPackageList(truck2, truck2_package_logs[1]) # Time Complexity: O(n) where n is the number of packages

    # Deliver the last packages
    dispatch.truckDeliverPackages(truck1, end_time) # Time Complexity: O(n^k) where n is the number of addresses and k is the number of packages
    dispatch.truckDeliverPackages(truck2, end_time) # Time Complexity: O(n^k) where n is the number of addresses and k is the number of packages

    return (dispatch, truck1, truck2)


# Main function of the software and loop for the UI
def main():
    dispatch, truck1, truck2 = deliver()

    # UI
    while True:
        print('*' * 50)
        print("Welcome to the WGUPS package delivery system.")
        print("Please select an option from the menu below:")
        print("1. Print all package statuses and total mileage")
        print("2. Get a single package status with a time")
        print("3. Get all package statuses with a time")
        print("4. Exit")
        print('*' * 50)

        option = input("Please enter your selection: (1-4): ")
        match option:
            case '1':
                print(Package.printHeader())
                print(dispatch.packages)
                distance = truck1.distance + truck2.distance
                print(f"Total mileage: {distance:.1f}")
            case '2':
                package_id = input("Please enter the package id: ")
                time = input("Please enter the time: (HH:MM AM/PM): ")
                try:
                    time_obj = datetime.datetime.strptime(time, "%I:%M %p")
                    _dispatch, _, _ = deliver(end_time=time_obj.time())
                    package = _dispatch.packages.get(int(package_id))
                    print(Package.printHeader())
                    print(package)
                except ValueError:
                    print("Invalid package id or time. Please try again.")
            case '3':
                time = input("Please enter the time: (HH:MM AM/PM): ")
                try:
                    time_obj = datetime.datetime.strptime(time, "%I:%M %p")
                    _dispatch, _, _ = deliver(end_time=time_obj.time())
                    print(Package.printHeader())
                    print(_dispatch.packages)
                except ValueError:
                    print("Invalid time. Please try again.")
            case '4':
                print("Thank you for using the WGUPS package delivery system.")
                exit()
            case _:
                print("Invalid selection. Please try again.")
        print()


if __name__ == '__main__':
    main()
