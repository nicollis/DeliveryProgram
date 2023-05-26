from algorithms.node import Node


# Self-Adjusting Linked List
# This linked list will move the node to the head when it is accessed
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # Allow the user to iterate over the linked list
    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            yield current_node.data
            current_node = current_node.next

    # Makes printing the linked list easier
    def __str__(self):
        current_node = self.head
        string = ''
        while current_node is not None:
            string += f'{current_node}\n'
            current_node = current_node.next
        return string

    # Our self-adjusting linked list will move the node to the head
    # This works on the memory principal of locality of reference
    # as we pull objects the most used objects will naturally be closer to the head
    # and quicker to access
    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def get(self, key):
        current_node = self.head
        previous_node = None
        while current_node is not None:
            if current_node.key == key:
                if self.head != current_node:
                    # Move the node to the head
                    previous_node.next = current_node.next
                    current_node.next = self.head
                    self.head = current_node
                return current_node.data
            previous_node = current_node
            current_node = current_node.next
        raise KeyError(key)

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def append(self, key, data):
        new_node = Node(key, data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        current_node = self.tail
        current_node.next = new_node  # type: ignore
        self.tail = new_node

    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def update(self, key, data):
        current_node = self.head
        while current_node is not None:
            if current_node.key == key:
                current_node.data = data
                return
            current_node = current_node.next
        raise KeyError(key)

    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def remove(self, key):
        current_node = self.head
        previous_node = None
        while current_node is not None:
            # Key found
            if current_node.key == key:
                # If the node is the head
                if previous_node is None:
                    self.head = current_node.next
                    # if this is the only node in the list
                    if self.tail == current_node: self.tail = None
                    del current_node
                    return
                # If the node is the tail
                if current_node.next is None:
                    self.tail = previous_node
                    previous_node.next = None
                    del current_node
                    return
                # If the node is in the middle
                previous_node.next = current_node.next
                del current_node
                return
            previous_node = current_node
            current_node = current_node.next
        raise KeyError(key)

    # Unused but useful
    # Time Complexity: O(n)
    # Space Complexity: O(n)
    def copy(self):
        new_list = LinkedList()
        current_node = self.head
        while current_node is not None:
            new_list.append(current_node.key, current_node.data)
            current_node = current_node.next
        return new_list
