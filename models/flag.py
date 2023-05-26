class Flag:
    ONLY_TRUCK_2 = "Can only be on truck 2"
    DELIVER_WITH_OTHER_PACKAGES = "Must be delivered with 13, 15, 19"
    DELAYED = "Delayed on flight---will not arrive to depot until 9:05 am"
    WRONG_ADDRESS = "Wrong address listed"
    FLAGS = [ONLY_TRUCK_2, DELIVER_WITH_OTHER_PACKAGES, DELAYED, WRONG_ADDRESS]

    def __init__(self, key, description=""):
        self.key = key
        self.description = description
