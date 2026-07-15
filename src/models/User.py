class User:
    def __init__(self, id, name, weight, height, measurements={}):
        self.id = id
        self.name = name
        self.weight = weight
        self.height = height
        self.measurements = measurements
        self.user_folder = self.get_folder()

    def __repr__(self):
        return f"<User {self.name} ({self.user_id})>"

    @classmethod
    def from_json(cls, data_dict):
        return cls(id=data_dict["id"], name=data_dict["name"], weight=data_dict["weight"], height=data_dict["height"],
                   measurements=data_dict["measurements"])
    
    def to_json(self):
        return {"id": self.id, "name": self.name, "weight": self.weight, "height": self.height,
                "measurements": self.measurements, "user_folder": self.user_folder}

    def set_weight(self, weight):
        self.weight = weight
    def set_height(self, height):
        self.height = height

    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_folder(self):
        return f"data/users/{self.id}" if self.id != "admin" else f"data/default"
    def get_weight(self):
        return self.weight
    def get_height(self):
        return self.height