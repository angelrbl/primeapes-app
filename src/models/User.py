class User:
    def __init__(self, user_id, name, weight, height, measurments={}, macrocycles=[]):
        self.user_id = user_id
        self.name = name
        self.weight = weight
        self.height = height
        self.measurments = measurments
        self.macrocycles = macrocycles
        self.user_folder = self.get_folder()

    def __repr__(self):
        return f"<Muscle {self.name}>"

    @classmethod
    def from_json(cls, data_dict):
        return cls(user_id=data_dict["user_id"], name=data_dict["name"], weight=data_dict["weight"], height=data_dict["height"],
                   measurments=data_dict["measurments"], macrocycles=data_dict["macrocycles"])
    
    def to_json(self):
        return {"user_id": self.user_id, "name": self.name, "weight": self.weight, "height": self.height,
                "measurments": self.measurments, "macrocycles": self.macrocycles, "user_folder": self.user_folder}

    def set_weight(self, weight):
        self.weight = weight
    def set_height(self, height):
        self.height = height

    def get_name(self):
        return self.name
    def get_id(self):
        return self.user_id
    def get_folder(self):
        return f"data/users/{self.user_id}" if self.user_id != "admin" else f"data/default"
    def get_weight(self):
        return self.weight
    def get_height(self):
        return self.height
