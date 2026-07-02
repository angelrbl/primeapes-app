from src.models.Muscle import Muscle

class Exercise:
    def __init__(self, name, primary_muscles = [], secondary_muscles=[]):
        self.name = name
        self.primary_muscles = primary_muscles
        self.secondary_muscles = secondary_muscles
    
    def __repr__(self):
        return f"<Exercise {self.name}>"

    @classmethod
    def from_json(cls, data_dict, muscle_map):
        primary_names = data_dict["primary_muscles"]
        secondary_names = data_dict["secondary_muscles"]

        primary_muscles = [muscle_map[name] for name in primary_names]
        secondary_muscles = [muscle_map[name] for name in secondary_names]
        return cls(name=data_dict["name"], primary_muscles=primary_muscles, secondary_muscles=secondary_muscles)
    
    def to_json(self):
        return {
            "name": self.name,
            "primary_muscles": self.get_primary_muscles_names(),
            "secondary_muscles": self.get_secondary_muscles_names()
        }

    def get_primary_muscles_names(self):
        return Muscle.to_name_list(self.primary_muscles)
    
    def get_primary_muscles(self):
        return self.primary_muscles

    def set_primary_muscles(self, muscles_list):
        self.primary_muscles = muscles_list

    def get_secondary_muscles(self):
        return self.secondary_muscles

    def get_secondary_muscles_names(self):
        return Muscle.to_name_list(self.secondary_muscles)
    
    def set_secondary_muscles(self, muscles_list):
        self.secondary_muscles = muscles_list

    def get_name(self):
        return self.name
    
    @staticmethod
    def to_name_list(exercises_list):
        exercise_names = []
        for exercise in exercises_list:
            exercise_names.append(exercise.get_name())
        return exercise_names 
