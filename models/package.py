from flag import Flag

class Package:
  def __init__(self, id, address, city, zip, deadline, weight, flags, group_number = None):
    self.id = id
    self.address = address
    self.city = city
    self.zip = zip
    self.deadline = deadline
    self.weight = weight
    self.flags = flags
    self.group_number = group_number
    self.truck = None

  def __str__(self):
    flags = ", ".join([flag.key for flag in self.flags])
    return f"{self.id} {self.address} {self.city} {self.zip} {self.deadline} {self.weight} flags({flags})"
    
    