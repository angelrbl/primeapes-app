class User:
    def __init__(self, user_id, name, weight, height):
        self.user_id = user_id
        self.name = name
        self.weight = weight
        self.height = height
        self.measurments = {}
        self.macrocycles = []

    def __repr__(self):
        return f"<Muscle {self.name}>"

    @classmethod
    def from_json(cls, data_dict):
        return cls(user_id=data_dict["user_id"], name=data_dict["name"], weight=data_dict["categories"], height=data_dict["height"], measurments=data_dict["measurments"], macrocycles=data_dict["macrocycles"])
    
    def to_json(self):
        return {"user_id": self.user_id, "name": self.name, "weight": self.weight, "height": self.height, "measurments": self.measurments, "macrocycles": self.macrocycles}

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.user_id