from src.models.Muscle import Muscle

class Exercise:
    def __init__(self, name, primary_muscles = [], secondary_muscles=[]):
        self.name = name
        self.primary_muscles = primary_muscles
        self.secondary_muscles = secondary_muscles
    
    def __repr__(self):
        return f"<Exercise {self.name}>"

    @classmethod
    def from_json(cls, data_dict):
        return cls(name=data_dict["name"], primary_muscles=data_dict["primary_muscles"], secondary_muscles=data_dict["secondary_muscles"])
    
    def to_json(self):
        return {
            "name": self.name,
            "primary_muscles": Muscle.to_list(self.primary_muscles),
            "secondary_muscles": Muscle.to_list(self.secondary_muscles)
        }

    def get_primary_muscles_list(self):
        return Muscle.to_list(self.primary_muscles)

    def get_secondary_muscles_list(self):
        return Muscle.to_list(self.secondary_muscles)
    
    def get_name(self):
        return self.name