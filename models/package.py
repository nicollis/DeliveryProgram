from models.flag import Flag
from models.status import Status

class Package:
  def __init__(self, id, address, zip, deadline, weight, flag, group_number=None):
    self.id = id
    self.address = address
    self.zip = zip
    self.deadline = deadline
    self.weight = weight
    self.flag = flag
    self.group_number = group_number
    self.truck = None
    self.status=Status.HUB
    self.delivery_time = None

  def __str__(self):
    return f"{self.id} {self.status} {self.address} {self.zip} {self.deadline} {self.weight} {self.flag} {self.delivery_time})"
    
    