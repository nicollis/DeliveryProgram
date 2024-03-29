import datetime

from models.flag import Flag
from models.status import Status


class Package:
    def __init__(self, id, address, city, zip, deadline, weight, flag):
        self.id = id
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline
        # Helper value so we don't have to keep converting deadline to datetime
        if deadline != 'EOD':
            self.deadline_as_time = datetime.datetime.combine(datetime.date.today(),
                                                              datetime.datetime.strptime(deadline, '%I:%M %p').time())
        else:
            self.deadline_as_time = None
        self.weight = weight
        self.flag = flag
        self.truck = None
        self.status = Status.HUB if flag != Flag.DELAYED or flag != Flag.WRONG_ADDRESS else Status.DELAYED
        self.delivery_time = None

    # Our function for printing the required information for a package
    def __str__(self):
        dt = self.delivery_time.strftime("%I:%M %p") if self.delivery_time else "N/A"

        if self.delivery_time is None:
            on_time = "N/A"
        elif self.deadline == 'EOD' or \
                datetime.datetime.combine(datetime.date.today(),
                                          datetime.datetime.strptime(self.deadline,'%I:%M %p').time()
                                          ) >= datetime.datetime.combine(datetime.date.today(), self.delivery_time):
            on_time = "YES"
        else:
            on_time = "NO"

        return "{:<3}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<35}".format(self.id, self.status, self.weight,
                                                                              self.deadline, dt, on_time, self.address)

    # Our function for printing the header for the package table
    @staticmethod
    def printHeader():
        return "{:<3}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<35}".format("ID", "STATUS", "WEIGHT", "DEADLINE",
                                                                      "DELIVERY TIME", "ON TIME", "ADDRESS")
