class Node:
    # because we are not allowed to use the built-in dictionary data structure
    # we will use a linked list to store the key-value pairs
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.next = None

    def __str__(self):
        return f'{self.data}'