import csv

from algorithms.hashtable import HashTable
from models.package import Package
from models.truck import Truck
from models.dispatch import Dispatch

# read data from package.csv and load into our hash table
# O(n) where n is the number of packages
def loadPageData():
    packages = HashTable()
    with open('data/packages.csv') as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            try: 
                package = Package(int(row[0]), row[1], int(row[4]), row[5], int(row[6]), row[7]) # todo: classify flags
                packages.append(package.id, package)
            except ValueError as e:
                print(f"Problem loading the package with id: {row[0]} into the hash table.\n {e}")
    return packages

def loadDistanceData():
    addresses = []
    distances = []
    with open('data/distances.csv') as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            row[0] = row[0].split('\n')[1].strip()
            addresses.append(row[0])
            distances.append([float(dist) for dist in row[2:]])

    return (addresses, distances)


def main():
    # Load in the packages
    packages = loadPageData()
    # Load in the distances
    addresses, distances = loadDistanceData()

    HUB = addresses[0] # the hub is the first address in the list

    truck1 = Truck(1, current_location=HUB)
    truck2 = Truck(2, current_location=HUB)
    truck_histories = [{}, {}]

    dispatch = Dispatch(HUB, packages, addresses, distances)

    # Load the packages into the trucks
    dispatch.truckLoadPackages(truck1)
    dispatch.truckLoadPackages(truck2)

    truck_histories[0].update(dispatch.truckDeliverPackages(truck1))
    truck_histories[1].update(dispatch.truckDeliverPackages(truck2))

    dispatch.truckLoadPackages(truck1)
    dispatch.truckLoadPackages(truck2)

    truck_histories[0].update(dispatch.truckDeliverPackages(truck1))
    truck_histories[1].update(dispatch.truckDeliverPackages(truck2))


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
                print(dispatch.packages)
                distance = truck1.distance + truck2.distance
                print(f"Total mileage: {distance:.1f}")
            case '2':
                package_id = input("Please enter the package id: ")
                try:
                    package = dispatch.packages.get(int(package_id))
                    print(package)
                except ValueError:
                    print("Invalid package id. Please try again.")
            case '3':
                time = input("Please enter the time: ")
                print(dispatch.packages)
            case '4':
                print("Thank you for using the WGUPS package delivery system.")
                exit()
            case _:
                print("Invalid selection. Please try again.")
        print()


    

    
    
            
if __name__ == '__main__':
    main()
