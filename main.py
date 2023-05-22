import csv

from algorithms.hashtable import HashTable
from models.package import Package

# read data from package.csv and load into our hash table
# O(n) where n is the number of packages
def loadPageData():
    packages = HashTable()
    with open('data/package.csv') as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            try: 
                package = Package(int(row[0]), row[1], int(row[4]), row[5], int(row[6]), row[7]) # todo: classify flags
                packages.append(package.id, package)
            except ValueError as e:
                print(f"Problem loading the package with id: {row[0]} into the hash table.\n {e}")
    return packages



def main():
    packages = loadPageData()
    print(packages)
    
            
if __name__ == '__main__':
    main()
