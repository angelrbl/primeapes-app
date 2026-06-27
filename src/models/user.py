class User:
    def __init__(self, name):
        self.name = name
        self.weight = None
        self.height = None
        self.measurments = None
        self.macrocycles = None

    def get_name(self):
        return self.name