class Muscle:
    def __init__(self, name):
        self.name = name
        self.categories = []

    def add_category(self, category):
        self.categories.append(category)