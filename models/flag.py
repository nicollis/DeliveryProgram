class Flag:
    ONLY_TRUCK_2 = "Only truck 2"
    DELIVER_WITH_OTHER_PACKAGES = "Deliver with other packages"
    DELAYED = "Delayed"
    WRONG_ADDRESS = "Wrong address"
    FLAGS = [ONLY_TRUCK_2, DELIVER_WITH_OTHER_PACKAGES, DELAYED, WRONG_ADDRESS]

    def __init__(self, key, description=""):
        self.key = key
        self.description = description