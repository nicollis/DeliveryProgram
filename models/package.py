import datetime

from models.flag import Flag
from models.status import Status

class Package:
  def __init__(self, id, address, city, zip, deadline, weight, flag, group_number=None):
    self.id = id
    self.address = address
    self.city = city
    self.zip = zip
    self.deadline = deadline
    self.weight = weight
    self.flag = flag
    self.group_number = group_number
    self.truck = None
    self.status=Status.HUB
    self.delivery_time = None

  def __str__(self):
    dt = self.delivery_time.strftime("%I:%M %p") if self.delivery_time else "N/A"
    return "{:<3}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<35}".format(self.id, self.status, self.weight, self.deadline, dt, self.address)

  @staticmethod
  def printHeader():
    return "{:<3}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<35}".format("ID", "STATUS", "WEIGHT", "DEADLINE", "DELIVERY TIME", "ADDRESS")
    
    