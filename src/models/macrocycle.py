class Macrocycle:
    def __init__(self, name, start_date, length):
        self.name = name
        self.start_date = start_date
        self.length = length
        self.microcycles = [None * length]

    def add_microcycle(self, microcycle_index, microcycle):
        self.microcycles[microcycle_index] = microcycle