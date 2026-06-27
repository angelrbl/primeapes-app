class Exercise:
    def __init__(self, name):
        self.name = name
        self.main_muscles = []
        self.secondary_muscles = []
    
    def get_name(self):
        return self.name