from src.models.Microcycle import Microcycle

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

    def clear_microcycles(self):
        for microcycle in self.microcycles:
            print(microcycle.get_workouts())
            microcycle.clear_workouts()
            print(microcycle.get_workouts())
        return True

    def get_muscle_sets(self):
        muscle_sets = {}
        for microycle in self.microcycles:
                muscle_sets.update(microycle.get_muscle_sets(muscle_sets))
        return muscle_sets

    def get_microcycles_muscle_sets(self):
        microcycles_muscle_sets = []
        for i in range(len(self.microcycles)):
            muscle_sets = self.microcycles[i].get_muscle_sets(muscle_sets={})
            for muscle, sets in muscle_sets.items():
                microcycles_muscle_sets.append({"Microcycle": f"M{i+1}", "Muscle": muscle, "Sets": sets})
        return microcycles_muscle_sets

    def get_description(self):
        return self.description
    def get_date(self):
        return self.start_date
    def get_name(self):
        return self.name
    def get_microcycles(self):
        return self.microcycles
    def get_microcycle(self, microcycle_index):
        return self.microcycles[microcycle_index]
    def get_microcycle_length(self):
        return self.microcycle_length
    def get_length(self):
        return self.length