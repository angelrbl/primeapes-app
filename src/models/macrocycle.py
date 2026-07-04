class Macrocycle:
    def __init__(self, name, start_date, length, microcycles = None):
        self.name = name
        self.start_date = start_date
        self.length = length
        self.microcycles = microcycles if microcycles else [None * length]

    def __repr__(self):
        return f"<Macrocycle {self.name}>"

    @classmethod
    def from_json(cls, data_dict, microcycle_map):
        microcycle_ids = data_dict["microcycles"]
        microcycles = [microcycle_map[microcycle_id] for microcycle_id in microcycle_ids]
        return cls(name=data_dict["name"], start_date=data_dict["start_date"], length=data_dict["length"], microcycles=microcycles)
    
    def to_json(self):
        return {
            "name": self.name,
            "start_date": self.start_date,
            "length": self.length,
            "microcycles": [microcycle.get_id() for microcycle in self.microcycles]
        }

    def add_microcycle(self, microcycle_index, microcycle):
        self.microcycles[microcycle_index] = microcycle