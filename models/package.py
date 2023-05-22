from models.flag import Flag

class Package:
  def __init__(self, id, address, zip, deadline, weight, flag, group_number = None):
    self.id = id
    self.address = address
    self.zip = zip
    self.deadline = deadline
    self.weight = weight
    self.flag = flag
    self.group_number = group_number
    self.truck = None

  def __str__(self):
    return f"{self.id} {self.address} {self.zip} {self.deadline} {self.weight} {self.flag})"
    
    