from src.models.Muscle import Muscle

class Exercise:
    def __init__(self, name, primary_muscles = [], secondary_muscles=[]):
        self.name = name
        self.primary_muscles = primary_muscles
        self.secondary_muscles = secondary_muscles
    
    def __repr__(self):
        return f"<Exercise {self.name}>"

    @classmethod
    def from_json(cls, data_dict, user):
        return cls(name=data_dict["name"], primary_muscles=Muscle.list_to_obj(data_dict["primary_muscles"], user=user), secondary_muscles=Muscle.list_to_obj(data_dict["secondary_muscles"], user=user))
    
    def to_json(self):
        return {
            "name": self.name,
            "primary_muscles": self.get_primary_muscles(),
            "secondary_muscles": self.get_secondary_muscles()
        }

    def get_primary_muscles(self):
        return Muscle.to_list(self.primary_muscles)

    def set_primary_muscles(self, muscles_list, user):
        if len(muscles_list) == 0:
            return None
        elif type(muscles_list[0]) == str:
            self.primary_muscles = Muscle.list_to_obj(muscles_list, user)
            return
        elif type(muscles_list[0]) == object:
            self.primary_muscles = muscles_list
            return

    def get_secondary_muscles(self):
        return Muscle.to_list(self.secondary_muscles)
    
    def set_secondary_muscles(self, muscles_list, user):
        muscles_list = [muscle_name.lower().replace(" ", "_") for muscle_name in muscles_list]
        if len(muscles_list) == 0:
            return None
        elif type(muscles_list[0]) == str:
            self.secondary_muscles = Muscle.list_to_obj(muscles_list, user)
        elif type(muscles_list[0]) == object:
            self.secondary_muscles = muscles_list

    def get_name(self):
        return self.name