from src.models.Microcycle import Microcycle
from src.utils.database import load_json_data, save_json_data

class Macrocycle:
    def __init__(self, name, start_date, description, length, microcycle_length, microcycles = None):
        self.name = name
        self.start_date = start_date
        self.description = description
        self.length = length
        self.microcycle_length = microcycle_length
        self.microcycles = microcycles if microcycles else self.initialize_microcycles()

    def __repr__(self):
        return f"<Macrocycle {self.name}>"

    @classmethod
    def from_json(cls, data_dict, microcycle_map):
        microcycle_ids = data_dict["microcycles"]
        microcycles = [microcycle_map[microcycle_id] for microcycle_id in microcycle_ids]
        return cls(
            name=data_dict["name"],
            start_date=data_dict["start_date"],
            description=data_dict["description"],
            length=data_dict["length"],
            microcycle_length=data_dict["microcycle_length"],
            microcycles=microcycles
            )
    
    def to_json(self):
        return {
            "name": self.name,
            "start_date": self.start_date,
            "description": self.description,
            "length": self.length,
            "microcycles": [microcycle.get_id() for microcycle in self.microcycles],
            "microcycle_length": self.microcycle_length
        }

    def initialize_microcycles(self):
        microcycles = []
        for i in range(self.length):
            microcycles.append(Microcycle(microcycle_id=f"{self.name}_w{i}", week_index=i, length=self.microcycle_length))
        return microcycles

    def add_microcycle(self, microcycle_index, microcycle):
        self.microcycles[microcycle_index] = microcycle

    def get_description(self):
        return self.description
    def get_date(self):
        return self.start_date
    def get_name(self):
        return self.name
    def get_microcycles(self):
        return self.microcycles
    def get_microcycle_length(self):
        return self.microcycle_length
    def get_length(self):
        return self.length