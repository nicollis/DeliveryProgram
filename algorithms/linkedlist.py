from algorithms.node import Node

class LinkedList:
  def __init__(self):
    self.head = None
    self.tail = None

  def __str__(self):
    current_node = self.head
    string = ''
    while current_node is not None:
      string += f'{current_node}\n'
      current_node = current_node.next
    return string
  
  # O(n)
  def get(self, key):
    current_node = self.head
    while current_node is not None:
      if current_node.key == key:
        return current_node.data
      current_node = current_node.next
    raise KeyError(key)

  # O(1)
  def append(self, key, data):
    new_node = Node(key, data)
    if self.head == None:
      self.head = new_node
      self.tail = new_node
      return
    current_node = self.tail
    current_node.next = new_node # type: ignore
    self.tail = new_node

  # O(n)
  def update(self, key, data):
    current_node = self.head
    while current_node is not None:
      if current_node.key == key:
        current_node.data = data
        return
      current_node = current_node.next
    raise KeyError(key)
  

  # O(n)
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
